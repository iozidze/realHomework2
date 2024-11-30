import pytest
import os
from visualizer import parse_config, parse_pom, generate_plantuml

def test_parse_config():
    config = parse_config("test_config.xml")
    assert config["visualizer_path"] == "/path/to/plantuml.jar"
    assert config["repository_url"] == "https://repo.maven.apache.org/maven2"

def test_parse_pom():
    dependencies = parse_pom("tests/sample_pom.xml")
    assert "org.springframework:spring-core" in dependencies
    assert dependencies["org.springframework:spring-core"] == "5.3.9"

def test_generate_plantuml(tmp_path):
    dependencies = {
        "org.springframework:spring-core": "5.3.9",
        "com.google.guava:guava": "30.1.1-jre"
    }
    output_path = tmp_path / "output.png"
    uml_path = generate_plantuml(dependencies, output_path)т о                                                                                                                      о
    assert uml_path.exists()
    with open(uml_path) as f:
        content = f.read()
        assert '"org.springframework\\nspring-core\\n5.3.9"' in content
