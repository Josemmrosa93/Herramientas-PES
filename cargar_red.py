import pandas as pd
import math
import re

def extraer_codigo_coche(texto: str):
    """De '891.1 - C4328 - ...' saca 'C4328'."""
    if not isinstance(texto, str):
        return None
    m = re.search(r"C\d{4}[A-Z]?", texto)
    return m.group(0) if m else None

def cargar_red(path_excel: str) -> dict:
    df = pd.read_excel(
        path_excel,
        sheet_name="Train IP Addressing (ECN)",  # tu hoja
        header=None
    )
    # xls = pd.ExcelFile(path_excel)
    # print("Hojas disponibles en el archivo Excel:")
    # for sheet_name in xls.sheet_names:
    #     print(f"- {sheet_name}")

    # print(df.iloc[19:45, 24:60])  # inspeccionar un trozo de la hoja
    

    # CONFIG DE TU HOJA
    COACH_ROW = 19          # fila donde están los nombres de coche
    FIRST_COACH_COL = 24    # columna Y = 24 (A=0 ... Y=24)
    UP_HEADER_ROW = 21      # fila donde pone "ID" arriba
    UP_PORT_START = 23
    UP_PORT_END = 32

    LOW_HEADER_ROW = 39     # fila donde pone "ID" abajo
    LOW_PORT_START = 41
    LOW_PORT_END = 50

    ncols = df.shape[1]

    # 1) localizar las columnas donde REALMENTE hay un coche
    coach_starts = []
    for c in range(FIRST_COACH_COL, ncols):
        cell = df.iat[COACH_ROW, c]
        code = extraer_codigo_coche(cell)
        if code:
            coach_starts.append(c)

    coach_starts.sort()

    tren = {}

    for i, start_col in enumerate(coach_starts):
        raw_text = df.iat[COACH_ROW, start_col]
        coach_code = extraer_codigo_coche(raw_text) or str(raw_text)

        # límite de columnas de ESTE coche
        end_col = coach_starts[i + 1] if i + 1 < len(coach_starts) else ncols

        coach_dict = {}

        # ----------- SWITCHES DE ARRIBA -----------
        for col in range(start_col + 1, end_col):
            if df.iat[UP_HEADER_ROW, col] == "ID":
                name_cell = df.iat[UP_PORT_START + 1, col]
                if isinstance(name_cell, str) and name_cell.strip():
                    sw_name = name_cell.strip()
                else:
                    sw_name = f"SW_{col}"

                ports = {}
                for r in range(UP_PORT_START, UP_PORT_END + 1):
                    port_name = df.iat[r, col + 1]
                    if not isinstance(port_name, str) or not port_name.strip():
                        continue

                    vlan = df.iat[r, col + 3]
                    device = df.iat[r, col + 4] if (col + 4) < ncols else None
                    if isinstance(device, float) and math.isnan(device):
                        device = None

                    ports[port_name.strip()] = {
                        "VLAN": int(vlan) if pd.notna(vlan) else None,
                        "Device": device,
                    }

                coach_dict[sw_name] = ports

        # ----------- SWITCHES DE ABAJO -----------
        for col in range(start_col + 1, end_col):
            if df.iat[LOW_HEADER_ROW, col] == "ID":
                name_cell = df.iat[LOW_PORT_START + 1, col]
                if isinstance(name_cell, str) and name_cell.strip():
                    sw_name = name_cell.strip()
                else:
                    sw_name = f"SW_low_{col}"

                ports = {}
                for r in range(LOW_PORT_START, LOW_PORT_END + 1):
                    port_name = df.iat[r, col + 1]
                    if not isinstance(port_name, str) or not port_name.strip():
                        continue

                    vlan = df.iat[r, col + 3]
                    device = df.iat[r, col + 4] if (col + 4) < ncols else None
                    if isinstance(device, float) and math.isnan(device):
                        device = None

                    ports[port_name.strip()] = {
                        "VLAN": int(vlan) if pd.notna(vlan) else None,
                        "Device": device,
                    }

                coach_dict[sw_name] = ports

        tren[coach_code] = coach_dict

    return tren


# USO
if __name__ == "__main__":
    tren = cargar_red("F073_IP_Ports_Addressing_00_38.xlsm")
    print(tren.keys())
    # print(tren["C4328"])
