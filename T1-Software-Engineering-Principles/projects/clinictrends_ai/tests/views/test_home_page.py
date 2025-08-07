import pytest
from streamlit.testing.v1 import AppTest

def test_home_page_renders_correctly():
    # Arrange
    app = AppTest.from_file("views/HomePage.py")
    
    # Act
    app.run()
    
    # Assert
    # Check the main title
    assert "ClinicTrends AI" in app.title[0].value
    
    # Check for key sections
    markdown_texts = [md.value for md in app.markdown]
    assert any("Visualize data" in text for text in markdown_texts)
    assert any("Measure NPS" in text for text in markdown_texts)
    
    # # Check for feature cards content
    feature_sections = [text for text in markdown_texts if "#### " in text]
    assert len(feature_sections) >= 3  # Should have at least 3 feature cards
    assert any("NPS" in text for text in feature_sections)
    assert any("Sentiment" in text for text in feature_sections)
    assert any("Translation" in text for text in feature_sections)

def test_navigation_instructions_exist():
    # Arrange
    app = AppTest.from_file("views/HomePage.py")
    
    # Act
    app.run()
    app.button("unlock_features").click().run()  # Simulate click
    
    # Assert
    # Check for navigation instructions in info boxes
    assert any("Use the sidebar" in info.value for info in app.info)
    assert any("navigate between different sections" in info.value for info in app.info)