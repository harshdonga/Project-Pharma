import logging
import datetime

from sawtooth_med.processor.med_payload import MedPayload
from sawtooth_med.processor.med_state import Medicine
from sawtooth_med.processor.med_state import MedState
from sawtooth_med.processor.med_state import MED_NAMESPACE

from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InternalError
from sawtooth_sdk.processor.exceptions import InvalidTransaction


LOGGER = logging.getLogger(__name__)

class MedicineHandler(TransactionHandler):

    @property
    def family_name(self):
        return('med')

    @property
    def family_versions(self):
        return(['1.0'])

    @property
    def namespaces(self):
        return([MED_NAMESPACE])

    def apply(self, transaction , context):

        header = transaction.header
        signer = header.signer_public_key

        med_payload = MedPayload.from_bytes(transaction.payload)

        med_state = MedState(context)

        if med_payload.action == 'createMedicine':
            if med_state.get_medicine(med_payload.medicineName) is not None:
                raise InvalidTransaction('Invalid action: Medicine already exists: {}'.format(med_payload.medicineName))

            medicine = Medicine(
                            medicineName = med_payload.medicineName,
                            medicineID = med_payload.medicineID,
                            medicineKeyContent = med_payload.medicineKeyContent,
                            medicineAllContents = med_payload.medicineAllContents,
                            manufactureDate = med_payload.manufactureDate,
                            expiryDate = med_payload.expiryDate,
                            stock = med_payload.stock,
                            manufacturerID = med_payload.manufacturerID,
                            owner = med_payload.newOwner,
                        )

            med_state.set_medicine(med_payload.medicineName , medicine)
            _display('Manufacturer: {} created medicine'.format(signer[:6]))



        elif(med_payload.action == 'updateMedicine'):
            medicine = med_state.get_medicine(med_payload.medicineName)
            if medicine:
                if(signer == medicine.manufacturerID):
                    medicine = Medicine(
                                        medicineName = med_payload.medicineName,
                                        medicineID = med_payload.medicineID,
                                        medicineKeyContent = med_payload.medicineKeyContent,
                                        medicineAllContents = med_payload.medicineAllContents,
                                        manufactureDate = med_payload.manufactureDate,
                                        expiryDate = med_payload.expiryDate,
                                        stock = med_payload.stock,
                                        manufacturerID = med_payload.manufacturerID,
                                        owner = med_payload.newOwner,
                                    )
                    med_state.set_medicine(med_payload.medicineName , medicine)
                    _display('Manufacturer: {} updated medicine successfully'.format(signer[:6]))
                else:
                    raise InvalidTransaction('Invalid action: UNAUTHORISED ACTION')
            else:
                raise InvalidTransaction('Invalid action: Medicine DOES NOT exists: {}'.format(med_payload.medicineName))


        elif(med_payload.action == 'updateMedicineOwner'):
            medicine = med_state.get_medicine(med_payload.medicineName)
            if medicine:
                if(med_payload.newOwner is not medicine.owner):
                    medicine.owner = med_payload.newOwner
                    med_state.set_medicine(med_payload.medicineName , medicine)
                    _display('Owner Updated by : {}'.format(signer[:6]))
                else:
                    raise InvalidTransaction('Invalid action UNAUTHORISED ACTION')
            else:
                raise InvalidTransaction('Invalid action: Medicine DOES NOT exists: {}'.format(med_payload.medicineName))



        elif med_payload.action == 'deleteMedicine':
            medicine = med_state.get_medicine(med_payload.medicineName)

            if medicine is None:
                raise InvalidTransaction('Invalid action: Medicine DOES NOT exists: {}'.format(med_payload.medicineName))

            if(signer == medicine.manufacturerID):
                med_state.delete_medicine(med_payload.medicineName)
                _display('Medicine Info deleted successfully by: {}'.format(signer[:6]))
            else:
                raise InvalidTransaction('Invalid action UNAUTHORISED ACTION')



        elif med_payload.action == 'produce':
            medicine = med_state.get_medicine(med_payload.medicineName)

            if medicine is None:
                raise InvalidTransaction('Invalid action: Medicine DOES NOT exists: {}'.format(med_payload.medicineName))

            if medicine.medicineID == med_payload.medicineID:
                medicine.stock = med_payload.stock
                med_state.set_medicine(med_payload.medicineName , medicine)

                _display('Medicine Info updated successfully by: {}'.format(signer[:6]))
            else:
                raise InvalidTransaction('Unhandled action: {}'.format(med_payload.action))

        else:
            raise InvalidTransaction('Unhandled action: {}'.format(med_payload.action))

def _display(msg):
    n = msg.count("\n")

    if n > 0:
        msg = msg.split("\n")
        length = max(len(line) for line in msg)
    else:
        length = len(msg)
        msg = [msg]
    LOGGER.debug("+" + (length + 2) * "-" + "+")
    for line in msg:
        LOGGER.debug("+ " + line.center(length) + " +")
    LOGGER.debug("+" + (length + 2) * "-" + "+")
