import xml.etree.ElementTree as ET
import argparse


def extract_talend_job_details(file_path):
    """
    Extrait les informations importantes d'un fichier .item de Talend.
    
    :param file_path: Chemin du fichier Talend (.item).
    :return: Un dictionnaire contenant les composants, connexions, métadonnées, contexte, routines et paramètres globaux.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 1. Extraction des composants Talend
    components = []
    for node in root.findall(".//node"):
        component = {
            "name": node.get("componentName"),
            "unique_name": node.find("./elementParameter[@name='UNIQUE_NAME']").get("value"),
            "position": (node.get("posX"), node.get("posY"))
        }
        components.append(component)

    # 2. Paramètres de chaque composant
    component_parameters = {}
    for node in root.findall(".//node"):
        unique_name = node.find("./elementParameter[@name='UNIQUE_NAME']").get("value")
        parameters = {
            param.get("name"): param.get("value")
            for param in node.findall("./elementParameter")
        }
        component_parameters[unique_name] = parameters

    # 3. Connexions entre composants
    connections = []
    for connection in root.findall(".//connection"):
        conn = {
            "source": connection.get("source"),
            "target": connection.get("target"),
            "type": connection.get("connectorName"),
            "label": connection.get("label")
        }
        connections.append(conn)

    # 4. Schéma des métadonnées
    metadata = {}
    for meta in root.findall(".//metadata"):
        component_name = meta.get("name")
        columns = []
        for column in meta.findall("./column"):
            columns.append({
                "name": column.get("name"),
                "type": column.get("type"),
                "nullable": column.get("nullable"),
                "default": column.get("defaultValue")
            })
        metadata[component_name] = columns

    # 5. Contexte défini
    context = []
    for ctx in root.findall(".//context"):
        context.append({
            "name": ctx.get("name"),
            "confirmationNeeded": ctx.get("confirmationNeeded")
        })

    # 6. Routines utilisées
    routines = []
    for routine in root.findall(".//routinesParameter"):
        routines.append({
            "id": routine.get("id"),
            "name": routine.get("name")
        })

    # 7. Paramètres globaux
    global_parameters = {
        param.get("name"): param.get("value")
        for param in root.findall(".//parameters/elementParameter")
    }

    # Résultat final
    result = {
        "components": components,
        "component_parameters": component_parameters,
        "connections": connections,
        "metadata": metadata,
        "context": context,
        "routines": routines,
        "global_parameters": global_parameters
    }

    return result


if __name__ == "__main__":
    # Configurer l'argument parser
    parser = argparse.ArgumentParser(description="Analyse un fichier .item de Talend et extrait les détails importants.")
    parser.add_argument("file_path", type=str, help="Chemin du fichier .item à analyser.")
    args = parser.parse_args()

    # Traiter le fichier .item
    file_path = args.file_path
    try:
        job_details = extract_talend_job_details(file_path)

        # Affichage des résultats
        print("=== Composants ===")
        for component in job_details["components"]:
            print(component)

        print("\n=== Paramètres des composants ===")
        for name, params in job_details["component_parameters"].items():
            print(f"{name}: {params}")

        print("\n=== Connexions ===")
        for connection in job_details["connections"]:
            print(connection)

        print("\n=== Métadonnées ===")
        for name, columns in job_details["metadata"].items():
            print(f"{name}: {columns}")

        print("\n=== Contexte ===")
        for ctx in job_details["context"]:
            print(ctx)

        print("\n=== Routines ===")
        for routine in job_details["routines"]:
            print(routine)

        print("\n=== Paramètres globaux ===")
        for param, value in job_details["global_parameters"].items():
            print(f"{param}: {value}")

    except Exception as e:
        print(f"Erreur lors de l'analyse du fichier : {e}")
