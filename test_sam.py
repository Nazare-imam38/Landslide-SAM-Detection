from samgeo import SamGeo
import inspect

def test():
    print("Testing SamGeo initialization...")
    try:
        sam = SamGeo(model_type="vit_b")
        print(f"SamGeo object: {sam}")
        print("\nAttributes:")
        for name in dir(sam):
            if not name.startswith("__"):
                print(f" - {name}")
                
        print("\nPredict method signature:")
        try:
            sig = inspect.signature(sam.predict)
            print(f" sam.predict{sig}")
        except Exception as e:
            print(f" Error getting signature: {e}")
            
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    test()
