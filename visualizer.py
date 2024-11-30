import os
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_config(config_path):
    """
    Чтение конфигурационного файла.
    """
    tree = ET.parse(config_path)
    root = tree.getroot()
    config = {
        "visualizer_path": root.find("visualizer_path").text,
        "package_path": root.find("package_path").text,
        "output_path": root.find("output_path").text,
        "repository_url": root.find("repository_url").text,
    }
    return config


def analyze_dependencies(package_path):
    """
    Анализ зависимостей Java-пакета.
    """
    dependencies = {}
    for root, _, files in os.walk(package_path):
        for file in files:
            if file == "pom.xml":  # Maven конфигурация
                dependencies.update(parse_pom(os.path.join(root, file)))
    return dependencies


def parse_pom(pom_path):
    """
    Извлечение зависимостей из POM-файла.
    """
    tree = ET.parse(pom_path)
    root = tree.getroot()
    namespaces = {"m": "http://maven.apache.org/POM/4.0.0"}
    dependencies = {}
    for dependency in root.findall(".//m:dependency", namespaces):
        group_id = dependency.find("m:groupId", namespaces).text
        artifact_id = dependency.find("m:artifactId", namespaces).text
        version = dependency.find("m:version", namespaces).text
        dependencies[f"{group_id}:{artifact_id}"] = version
    return dependencies


def generate_plantuml(dependencies, output_path):
    """
    Генерация файла PlantUML.
    """
    plantuml_content = "@startuml\n"
    plantuml_content += "skinparam linetype ortho\n"
    for dep, version in dependencies.items():
        group, artifact = dep.split(":")
        plantuml_content += f'"{group}\\n{artifact}\\n{version}" --> "{artifact}"\n'
    plantuml_content += "@enduml\n"

    uml_path = Path(output_path).with_suffix(".puml")
    with open(uml_path, "w") as file:
        file.write(plantuml_content)
    return uml_path


def render_plantuml(plantuml_path, visualizer_path, output_path):
    """
    Рендеринг графа с помощью PlantUML.
    """
    subprocess.run(["java", "-jar", visualizer_path, plantuml_path, "-o", str(Path(output_path).parent)])


def main(config_path):
    """
    Основная функция.
    """
    config = parse_config(config_path)
    dependencies = analyze_dependencies(config["package_path"])
    uml_path = generate_plantuml(dependencies, config["output_path"])
    render_plantuml(uml_path, config["visualizer_path"], config["output_path"])
    print(f"Граф зависимостей успешно создан: {config['output_path']}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Использование: python visualizer.py <путь_к_конфигу>")
        sys.exit(1)
    main(sys.argv[1])
