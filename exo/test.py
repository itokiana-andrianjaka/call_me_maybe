from pydantic import BaseModel, model_validator, ValidationError, Field

class TestModel(BaseModel):
    name: str = Field(min_length=4)
    print("a")

    @model_validator(mode="before")
    def test_validation(self):
        try:
            if len(self.name) >= 4:
                raise ValueError("Name must be at least 5 characters long.")
        except (ValueError, ValidationError) as e:
            raise ValueError(f"error: {e}")

try:
    test = TestModel(name="Jo")
except (ValueError, ValidationError) as e:
    print(e.__class__.__name__)
