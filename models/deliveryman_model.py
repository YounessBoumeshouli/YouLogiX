import User
import Parcel
from etities.deliveryman_entity import Delivery_man
from entities.enums.Parcel_enum import Parcel_enum
from app.schemas.delivery_man import DeliveryManCreate
class Deliveryman(User):

    def assignParcel(self ,db, parcel_id)->bool:
        parcel =  Parcel.getParcel(parcel_id)
        return False if parcel.status == Parcel_enum.LIVRED else True
    def deliveryMan_create(self , delivery_man_in: DeliveryManCreate)->bool:
        delivery_man_data = delivery_man_in.model_dump()

        db_delivery_man = Client(
            **delivery_man_data,
            hashed_password=hashed_password
        )

        db.add(db_delivery_man)
        db.commit()
        db.refresh(db_delivery_man)
        return db_delivery_man
