
## Renting bot

Bot handles simple cases of __Greeting__, __Request__ and __Goodbye__ cases. For more reliable response one needs more real world training data, as well as, more stories.

## Try it out

Just call the already trained model by `python3 dialogue_management_model.py`  and rent a device.
Bot will detect device and period of renting, giving you the corresponding price tag.

## Known Issues

Rasa_nlu throws an error for Python 3.6. One workaround is installing a slightly older version of rasa_nlu.

Model was tested on Python 3.4.6.

## Changelog

- Now goodbye message contains price and device name
- Time exceptions are handled correctly now
- Minor changes
