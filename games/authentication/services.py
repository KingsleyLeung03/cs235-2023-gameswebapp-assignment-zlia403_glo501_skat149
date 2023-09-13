from werkzeug.security import generate_password_hash, check_password_hash

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass

def add_user(user_name: str, password: str, repo: AbstractRepository):
    
    # check if user name is already taken
    user = repo.get_user(user_name)
    if user is not None:
        raise NameNotUniqueException
    
    # genegate password hash to encript password
    password_hash = generate_password_hash(password)
    
    # create new user
    user = User(user_name, password_hash)
    repo.add_user(user)
    


    
    
    
    