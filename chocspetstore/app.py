from chocspetstore.entities import Category
from chocspetstore.entities import Pet
from chocspetstore.entities import PetStatus
from chocspetstore.entities import Photo
from chocspetstore.repositories.pet_repository import PetRepository

repository = PetRepository()
pet = Pet(name="Pimpek", category=Category(name="special pets"), status=PetStatus.AVAILABLE)
pet.photos.append(Photo(name="test", url="http://petphotos.com/test"))


repository.create(pet)
