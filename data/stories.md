## story 01
* greet
    - utter_greet

## story 02
* goodbye
    - utter_goodbye

## story 03
* request
    - action_request

## story 04
* greet
    - utter_greet
* request
    - action_request

## story 05
* request
    - action_request
* goodbye
    - utter_goodbye

## story 06
* greet
    - utter_greet
* request
    - action_request
* goodbye
    - utter_goodbye

## story 07
* request{"device": "Vive"}
    - slot{"device": "Vive"}
    - action_request
    - slot{"device": "Vive"}
* goodbye
    - utter_goodbye
    - export

## story 08
* greet
    - utter_greet
* request
    - action_request
    - slot{"device": " "}
    - export

## Generated Story 7590461091971622044
* greet
    - utter_greet
* request{"device": "iphone 7"}
    - slot{"device": "iphone 7"}
    - action_request
    - slot{"device": "iphone 7"}
* goodbye
    - utter_goodbye
    - export

