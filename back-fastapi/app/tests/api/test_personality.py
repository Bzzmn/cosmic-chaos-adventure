from fastapi.testclient import TestClient


def test_get_personality_questions(client: TestClient) -> None:
    """
    Prueba el endpoint GET /api/personality/questions.
    
    Verifica que:
    1. El endpoint devuelve un código 200 OK
    2. La respuesta contiene una lista de preguntas
    3. Las preguntas incluyen los campos context_image y scenario_description
    4. Las opciones de respuesta incluyen todos los campos esperados
    """
    response = client.get("/api/personality/questions")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    question = data[0]
    
    # Verificar que la pregunta tiene todos los campos esperados
    assert "id" in question
    assert "question" in question
    assert "options" in question
    assert "created_at" in question
    assert "updated_at" in question
    
    # Verificar específicamente los nuevos campos añadidos
    assert "context_image" in question
    assert "scenario_description" in question
    
    # Verificar que los nuevos campos contienen los valores esperados
    assert question["context_image"] == "https://example.com/images/wormhole_closet.jpg"
    assert "Estación Espacial Zeta-9" in question["scenario_description"]
    
    # Verificar que las opciones tienen todos los campos esperados
    assert len(question["options"]) == 4
    
    option = question["options"][0]
    assert "text" in option
    assert "emoji" in option
    assert "value" in option
    assert "effect" in option
    assert "feedback" in option
    
    # Verificar que los efectos incluyen todas las estadísticas esperadas
    effect = option["effect"]
    assert "quantum_charisma" in effect
    assert "time_warping" in effect 