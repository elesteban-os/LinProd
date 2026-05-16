"""
Tests para la API de LinProd
Ejecutar con: pytest
"""

import pytest
from fastapi.testclient import TestClient
from app import app
from production_logic import simulador

client = TestClient(app)


class TestHealthCheck:
    """Tests para el endpoint de health check"""
    
    def test_health_check_returns_ok(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestEstado:
    """Tests para obtener el estado del sistema"""
    
    def test_obtener_estado(self):
        response = client.get("/estado")
        assert response.status_code == 200
        data = response.json()
        assert "t_actual" in data
        assert "ejecutando" in data
        assert "procesos" in data
        assert "eventos" in data
        assert "metricas" in data


class TestSimulacionControl:
    """Tests para controlar la simulación"""
    
    def test_start_simulacion(self):
        simulador.reset()
        response = client.post("/simulacion/control", json={"comando": "start"})
        assert response.status_code == 200
        assert response.json()["status"] == "success"
    
    def test_pause_simulacion(self):
        simulador.start()
        response = client.post("/simulacion/control", json={"comando": "pause"})
        assert response.status_code == 200
        assert response.json()["status"] == "success"
    
    def test_reset_simulacion(self):
        response = client.post("/simulacion/control", json={"comando": "reset"})
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert simulador.t_actual == 0
    
    def test_comando_invalido(self):
        response = client.post("/simulacion/control", json={"comando": "invalido"})
        assert response.status_code == 200
        assert response.json()["status"] == "error"


class TestProcesos:
    """Tests para gestión de procesos"""
    
    def test_obtener_procesos(self):
        response = client.get("/procesos")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_obtener_procesos_estructura(self):
        response = client.get("/procesos")
        data = response.json()
        assert "id" in data[0]
        assert "nombre" in data[0]
        assert "en_espera" in data[0]
        assert "tareas" in data[0]


class TestWebSocket:
    """Tests para WebSocket"""
    
    def test_websocket_connect(self):
        with client.websocket_connect("/ws/simulacion") as websocket:
            data = websocket.receive_json()
            assert "t_actual" in data
            assert "ejecutando" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
