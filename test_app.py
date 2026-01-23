import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHome:
    """Tests for the home route."""
    
    def test_home_route_returns_200(self, client):
        """Test that home route returns 200 status code."""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_home_route_returns_html(self, client):
        """Test that home route returns HTML content."""
        response = client.get('/')
        assert response.content_type == 'text/html; charset=utf-8'


class TestHealth:
    """Tests for the health check route."""
    
    def test_health_route_returns_200(self, client):
        """Test that health route returns 200 status code."""
        response = client.get('/health')
        assert response.status_code == 200
    
    def test_health_route_returns_json(self, client):
        """Test that health route returns JSON content."""
        response = client.get('/health')
        assert response.content_type == 'application/json'
    
    def test_health_route_response_structure(self, client):
        """Test that health route returns expected JSON structure."""
        response = client.get('/health')
        data = response.get_json()
        
        assert 'status' in data
        assert 'health' in data
        assert 'timestamp' in data
        assert data['status'] == 'ok'
        assert data['health'] == 'healthy'
    
    def test_health_route_has_valid_timestamp(self, client):
        """Test that health route returns a valid ISO format timestamp."""
        from datetime import datetime
        
        response = client.get('/health')
        data = response.get_json()
        
        # Verify timestamp is in ISO format and can be parsed
        try:
            datetime.fromisoformat(data['timestamp'])
        except ValueError:
            pytest.fail("Timestamp is not in valid ISO format")


class TestAppConfig:
    """Tests for app configuration."""
    
    def test_app_exists(self):
        """Test that Flask app is created."""
        assert app is not None
    
    def test_app_is_testing_mode(self):
        """Test that app can be set to testing mode."""
        app.config['TESTING'] = True
        assert app.config['TESTING'] is True
