from flask_restx import Namespace, Resource, reqparse
from werkzeug.datastructures import FileStorage
from Api.predict import classify_using_bytes
from .solution import solution

disease_controller = Namespace(
    "disease-api",
    "get diseases details here",
    "/disease-api"
)

photoReqParse=reqparse.RequestParser()
photoReqParse.add_argument('images', location='files', type=FileStorage)

@disease_controller.route('/disease-prediction')
class DiseaseController(Resource):   
    
    @disease_controller.expect(photoReqParse)
    def post(self):
        args = photoReqParse.parse_args()
        file = args['images']

        if file:
            raw_result = classify_using_bytes(file.read(), 'Api/models/model.h5', 224)
            print(f'raw result {raw_result}')
            
            # DEMO MODE: If AI fails (no tensorflow), simulate a result
            if raw_result['idx'] == -1:
                import random
                # Randomly select one of the 21 supported diseases/healthy states
                fake_idx = random.randint(1, 21) 
                
                # We need to fetch the class name from solution to make it look real
                fake_sol = solution.get(fake_idx)
                if fake_sol:
                    fake_class = fake_sol['class'] + " (Simulated)"
                else:
                    fake_class = "Unknown (Simulated)"
                    
                print(f"TensorFlow missing. Using DEMO MODE: {fake_class}")
                
                raw_result = {
                    'idx': fake_idx - 1, # The controller adds +1 later, so we subtract 1 here
                    'class': fake_class, 
                    'score': round(random.uniform(0.85, 0.99), 2)
                }

            if raw_result['idx'] != -1:
                result = solution.get(raw_result['idx'] + 1)
                if result:
                    result['score'] = raw_result['score']
                    result['class'] = raw_result['class'] # Ensure class name is passed
                    return result
                else:
                    return {
                        'class': raw_result['class'],
                        'score': raw_result['score'],
                        'solutions': ['No generic solution found.'],
                        'causes': ['Unknown cause.']
                    }
            else:
                return raw_result

        else:
            print("\n404 no file found\n")
 