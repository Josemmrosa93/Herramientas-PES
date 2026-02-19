import threading
import paramiko
import socket
import struct
import time


class isagrafInterface():

    class isaTypes():
        ISA_TYPSTRING = 6
        ISA_TYPLINT = 12
        ISA_TYPLREAL = 15

    MAX_VAR_PER_REQUEST = 50
    READ_ERROR = "Error!"
    VARIABLE_NOT_FOUND = "Variable not found"
    VARIABLE_OVERSIZE = "Variable oversize"
    VARIABLE_OUT_OF_MEM = "Variable out of mem"

    class msgHeader():

        def __init__(self, tag:bytearray, length:int, crc:bytearray, cmd_code:bytearray, packet_id:bytearray, msg_data:bytearray):
            self.tag = tag
            self.length = length
            self.crc = crc
            self.cmd_code = cmd_code
            self.packet_id = packet_id
            self.msg_data = msg_data


    def __init__(self, ip:str):
        self.__ip = ip
        self.__thread = None
        self.__port = 22
        self.__user = "root"
        self.__pass = "root"
        self.__timeout = 20
        self.__ssh_client = None
        self.__conn_mutex = threading.Lock()
        self.__connected = False
        self.__clientSocket = None
        self.__package_id = 1

        if ":" in ip:
            aux = ip.split(":")
            addr = aux[0]
            try:
                port = int(aux[1])
            except:
                port = 4101

        else:
            addr = ip
            port = 4101

        self.__addr = (addr, port)


    def __getFrameHeader(self, received_bytes:bytearray) -> msgHeader:

        msg_len = len(received_bytes) 
        if msg_len < 8:
            return None

        elif msg_len < 13:
            (tag, length, crc) = struct.unpack(">HIH", received_bytes[:8])
            cmd_code = None
            packet_id = None

        else:
            (tag, length, crc, cmd_code, packet_id) = struct.unpack(">HIHBI", received_bytes[:13])

        if tag != 0xAAAA:
            return None

        return isagrafInterface.msgHeader(tag, length, crc, cmd_code, packet_id, received_bytes[13:])


    def __getVarValue(self, var_def_raw:bytearray, data_area:bytearray) -> str:

        (var_size, var_type, var_def, var_offset) = struct.unpack(">IIII", var_def_raw)

        if var_size == 0xFFFFFFFF:
            return isagrafInterface.VARIABLE_NOT_FOUND

        elif var_offset == 0xFFFFFFFE:
            return isagrafInterface.VARIABLE_OVERSIZE

        elif var_offset + var_size > len(data_area):
            return isagrafInterface.VARIABLE_OUT_OF_MEM

        data_raw = data_area[var_offset:var_offset + var_size]


        # Parse type
        if var_def != 0:
            return data_raw

        # boolean
        elif var_type == 1:
            return True if struct.unpack(">?", data_raw)[0] else False

        # sint
        elif var_type == 2:
            return int(struct.unpack(">b", data_raw)[0])

        # dint
        elif var_type == 3:
            return int(struct.unpack(">i", data_raw)[0])

        # time
        elif var_type == 4:
            return int(struct.unpack(">I", data_raw)[0])

        # real
        elif var_type == 5:
            return float(struct.unpack(">f", data_raw)[0])

        # string
        elif var_type == 6:
            max_size = data_raw[0]
            size = data_raw[1]
            if size == 0:
                return ""
            elif len(data_raw) <= size+2:
                return data_raw[2:].decode('iso-8859-1')
            else:
                return data_raw[2:size+2].decode('iso-8859-1')

        # mem block
        elif var_type == 7:
            return data_raw

        # usint
        elif var_type == 8:
            return int(struct.unpack(">B", data_raw)[0])

        # int
        elif var_type == 9:
            return int(struct.unpack(">h", data_raw)[0])

        # uint
        elif var_type == 10:
            return int(struct.unpack(">H", data_raw)[0])

        # udint
        elif var_type == 11:
            return int(struct.unpack(">I", data_raw)[0])

        # lint
        elif var_type == 12:
            return int(struct.unpack(">q", data_raw)[0])

        # ulint
        elif var_type == 13:
            return int(struct.unpack(">Q", data_raw)[0])

        # date
        elif var_type == 14:
            return data_raw.hex()

        # lreal
        elif var_type == 15:
            return str(struct.unpack(">d", data_raw)[0])


        else:
            return data_raw


    def __getlockReleaseDataFromBytes(self, header:bytearray) -> list[bool]:

        # Get data
        if header.cmd_code != 0x91 and header.cmd_code != 0x92:
            return {}


        # Get var amount
        var_amount = struct.unpack(">I", header.msg_data[:4])[0]
        var_definition_bytes = var_amount
        if var_definition_bytes + 4 > len(header.msg_data):
            return {}


        # Get var definitions
        var_values = []
        data_area = header.msg_data[4:]
        for val in data_area:
            if val == 0:
                var_values.append(True)
            else:
                var_values.append(False)

        return var_values


    def __getwriteDataFromBytes(self, header:bytearray) -> list[bool]:

        # Get data
        if header.cmd_code != 0x92 and header.cmd_code != 0x82:
            return {}


        # Get var amount
        var_amount = struct.unpack(">I", header.msg_data[:4])[0]
        var_definition_bytes = var_amount
        if var_definition_bytes + 4 > len(header.msg_data):
            return []


        # Get var definitions
        var_values = []
        data_area = header.msg_data[4:]
        for val in data_area:
            if val == 0:
                var_values.append(True)
            else:
                var_values.append(False)

        return var_values


    def __getReadDataFromBytes(self, header:bytearray) -> list[str]:

        var_values = []

        # Get data
        if header.cmd_code != 0x81:
            return var_values


        # Get var amount
        var_amount = struct.unpack(">I", header.msg_data[:4])[0]
        var_definition_bytes = var_amount * 16
        if var_definition_bytes + 4 > len(header.msg_data):
            return var_values


        # Get var definitions
        data_area = header.msg_data[4 + var_definition_bytes:]
        read_offset = 4
        for i in range(var_amount):
            raw_var_structure = header.msg_data[read_offset:read_offset + 16]
            read_offset += 16
            value = self.__getVarValue(raw_var_structure, data_area)
            var_values.append(value)


        return var_values


    def __modbusCrc(self, msg:str) -> int:
        crc = 0xFFFF
        for n in range(len(msg)):
            crc ^= msg[n]
            for i in range(8):
                if crc & 1:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return crc


    def __sendReceiveFrame(self, cmd_code:bytearray, msg:bytearray, wait_time:int) -> bytearray:

        header = None

        if not self.__conn_mutex.acquire(blocking=True, timeout=wait_time):
            return header

        try:

            # Check socket
            if not self.__clientSocket:
                self.__clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__clientSocket.settimeout(3)
                self.__clientSocket.connect(self.__addr)
                self.__connected = True

            # message header
            packet_id = self.__package_id
            msg_header2 = struct.pack(">bI", cmd_code, packet_id)


            # inc package ID
            if self.__package_id > 0xFFFF:
                self.__package_id = 0
            else:
                self.__package_id += 1

            # Ethernet header
            tag = bytearray.fromhex("AAAA")
            msg_length = len(msg_header2 + msg)
            msg_length_bytes = struct.pack(">I", msg_length)

            crc_num = self.__modbusCrc(tag + msg_length_bytes)
            crc = struct.pack("<H", crc_num)
            msg_header = tag + msg_length_bytes + crc


            # Send
            self.__clientSocket.send(msg_header + msg_header2 + msg)


            # Read response
            input_bytes = bytearray()
            while True:
                read_bytes = self.__clientSocket.recv(1024)
                if not read_bytes:
                    break
                input_bytes += read_bytes
                header = self.__getFrameHeader(input_bytes)
                current_length = len(input_bytes)
                if header and header.packet_id:
                    if header.packet_id != packet_id:
                        input_bytes = bytearray()

                    elif header.length == current_length - 8:
                        break

        except:
            if self.__clientSocket:
                self.__clientSocket.close()
                self.__clientSocket = None
            self.__connected = False
            header = None


        self.__conn_mutex.release()
        return header


    def __readFromInterface(self, variables:list[str], wait_time:int=-1) -> dict[str, str]:

        rv = {}
        oversize_vars = []

        # read info
        var_amount = struct.pack(">I", len(variables))
        all_var_name = bytearray(0)
        for var_name in variables:
            var_name_bytes = var_name.encode()
            if len(var_name_bytes) < 80:
                var_name_bytes += bytearray(80 - len(var_name_bytes))
            all_var_name += var_name_bytes[:80]


        # Build msg
        msg_data = var_amount + all_var_name


        # Send frame
        header = self.__sendReceiveFrame(0x01, msg_data, wait_time)
        if header:

            # Process frame
            values = self.__getReadDataFromBytes(header)

            # Check values
            if len(values) == len(variables):

                for i in range(len(values)):
                    rv[variables[i]] = values[i]
                    if values[i] == isagrafInterface.VARIABLE_OVERSIZE:
                        oversize_vars.append(variables[i])

            else:
                for var in variables:
                    rv[var] = isagrafInterface.READ_ERROR

        else:
            for var in variables:
                rv[var] = isagrafInterface.READ_ERROR


        # Re-send oversize vars
        if len(oversize_vars) > 0 and len(oversize_vars) != len(variables) :
            rv |= self.__readFromInterface(oversize_vars, wait_time)

        return rv


    def __getVarIsagrafTypeAndSize(self, value:any) -> tuple[int, int]:

        try:
            int(value)
            return isagrafInterface.isaTypes.ISA_TYPLINT, 8
        except:
            pass

        try:
            float(value)
            return isagrafInterface.isaTypes.ISA_TYPLREAL, 8

        except:
            pass

        try:
            str(value)
            return isagrafInterface.isaTypes.ISA_TYPSTRING, 80
        except:
            pass



        return 0, 0


    def __writeFromInterface(self, variableMap:dict, lock:bool, wait_time:int) -> dict[str, bool]:

        rv = {}


        # Command code
        cmd_code = 0x12 if lock else 0x02


        # write info
        var_amount = struct.pack(">I", len(variableMap))
        write_var_info = bytearray(0)
        data_area = bytearray(0)
        for var_name in variableMap:

            # Var name
            var_name_bytes = var_name.encode()
            if len(var_name_bytes) < 80:
                var_name_bytes += bytearray(80 - len(var_name_bytes))
            write_var_info += var_name_bytes[:80]


            var_value = variableMap[var_name]

            # Var type, size
            var_type, var_size = self.__getVarIsagrafTypeAndSize(var_value)
            write_var_info += struct.pack(">bII", var_type, var_size, len(data_area) + var_size)


            # var offset
            if var_type == isagrafInterface.isaTypes.ISA_TYPLINT:
                data_area += struct.pack(">q", int(var_value))

            elif var_type == isagrafInterface.isaTypes.ISA_TYPLREAL:
                data_area += struct.pack(">d", float(var_value))

            elif var_type == isagrafInterface.isaTypes.ISA_TYPSTRING:
                if var_value.startswith("#"):
                    var_value = var_value[1:]
                var_value_bytes = var_value.encode()
                if len(var_value_bytes) < 80:
                    var_value_bytes += bytearray(80 - len(var_value))
                data_area += var_value_bytes[:80]


        # generate msg
        msg = var_amount + write_var_info + data_area


        # Send frame
        header = self.__sendReceiveFrame(cmd_code, msg, wait_time)


        # Process response
        if header:

            # Process frame
            values = self.__getwriteDataFromBytes(header)

            # Check values
            variables = list(variableMap.keys())
            if len(values) == len(variables):
                for i in range(len(values)):
                    rv[variables[i]] = values[i]
            else:
                for var in variableMap:
                    rv[var] = False

        else:
            for var in variableMap:
                rv[var] = False


        return rv


    def __lockFromInterface(self, variables:list, lock:bool, wait_time:int) -> dict[str, bool]:
        rv = {}

        # read info
        var_amount = struct.pack(">I", len(variables))
        all_var_name = bytearray(0)
        for var_name in variables:
            var_name_bytes = var_name.encode()
            if len(var_name_bytes) < 80:
                var_name_bytes += bytearray(80 - len(var_name_bytes))
            all_var_name += var_name_bytes[:80]


        # Build msg
        msg_data = var_amount + all_var_name


        cmd_code = 0x12 if lock else 0x11

        # Send frame
        header = self.__sendReceiveFrame(cmd_code, msg_data, wait_time)


        # Process response
        if header:

            # Process frame
            values = self.__getlockReleaseDataFromBytes(header)

            # Check values
            if len(values) == len(variables):
                for i in range(len(values)):
                    rv[variables[i]] = values[i]
            else:
                for var in variables:
                    rv[var] = False

        else:
            for var in variables:
                rv[var] = False


        return rv


    def __createConnectionObject() -> paramiko.SSHClient:
        ssh_obj = paramiko.SSHClient()
        ssh_obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        return ssh_obj


    def __executeCommand(self, commands:str, wait_time:int=-1) -> list[bool]:
        result = []

        if not self.__conn_mutex.acquire(blocking=True, timeout=wait_time):
            return


        # tmp solution. Disconnect
        if self.__clientSocket:
            self.__clientSocket = None


        if isinstance(commands, str):
            aux = commands
            commands = [aux]

        try:
            if not self.__ssh_client:
                self.__ssh_client = isagrafInterface.__createConnectionObject()
                self.__ssh_client.connect(self.__ip, self.__port, self.__user, self.__pass, timeout=self.__timeout)

            # Execute commands
            for command in commands:
                entrada, salida, error = self.__ssh_client.exec_command(command)
                stdout = salida.read().decode()
                stderr = error.read().decode()

                exec_result_code = salida.channel.recv_exit_status()
                if exec_result_code != 0:
                    result.append("Command Error!")
                elif stderr != "":
                    result.append("Read error!")
                else:
                    result.append(stdout)

        except:
            self.__ssh_client = None
            for i in range(0, len(commands) - len(result)):
                result.append("Connection error!")


        self.__conn_mutex.release()
        return result


    def readValues(self, variableMap:list[str], wait_time:int=-1) -> dict[int, dict[str, str]]:

        # Execute command
        results = {}
        while len(variableMap) != 0:
            if len(variableMap) > isagrafInterface.MAX_VAR_PER_REQUEST:
                req_batch = variableMap[:isagrafInterface.MAX_VAR_PER_REQUEST]
                variableMap = variableMap[isagrafInterface.MAX_VAR_PER_REQUEST:]
            else:
                req_batch = variableMap
                variableMap = []

            batch_result = self.__readFromInterface(req_batch, wait_time)

            if not self.__connected and len(variableMap) > 0:
                for var in variableMap:
                    batch_result[var] = isagrafInterface.READ_ERROR
                variableMap = []

            update_time = int(time.time_ns() / 1000000)
            if batch_result:
                if update_time not in results:
                    results[update_time] = batch_result
                else:
                    results[update_time] |= batch_result

        return results


    def writeValues(self, variableMap:dict, lock:bool, wait_time:int=-1) -> dict[int, dict[str, str]]:

        results = {}

        var_names = variableMap.keys()
        var_values = variableMap.values()
        while len(var_names) != 0:
            if len(var_names) > isagrafInterface.MAX_VAR_PER_REQUEST:
                req_batch_names = var_names[:isagrafInterface.MAX_VAR_PER_REQUEST]
                req_batch_values = var_values[:isagrafInterface.MAX_VAR_PER_REQUEST]
                var_names = var_names[isagrafInterface.MAX_VAR_PER_REQUEST:]
                var_values = var_values[isagrafInterface.MAX_VAR_PER_REQUEST:]
            else:
                req_batch_names = var_names
                req_batch_values = var_values
                var_names = []
                var_values = []

            batch_result = self.__writeFromInterface(dict(zip(req_batch_names, req_batch_values)), lock, wait_time)
            update_time = int(time.time_ns() / 1000000)
            if batch_result:
                if update_time not in results:
                    results[update_time] = batch_result
                else:
                    results[update_time] |= batch_result

        return results


    def lockValues(self, variableList:list[str], lock:bool, wait_time:int=-1) -> dict[int, list[str]]:

        results = {}

        for var in variableList:
            batch_result = self.__lockFromInterface([var], lock, wait_time)
            update_time = int(time.time_ns() / 1000000)
            if batch_result:
                if update_time not in results:
                    results[update_time] = batch_result
                else:
                    results[update_time] |= batch_result

        return results


    def isConnected(self) -> bool:
        return self.__connected