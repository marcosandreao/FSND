from fyyur import db
from fyyur.models import Venue


class BaseRepository:

    def delete_by_id(self, _id):
        model = Venue.query.get(_id)
        try:
            db.session.delete(model)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False
        finally:
            db.session.close()

    def persiste(self, model, throw_exception=False):
        try:
            db.session.add(model)
            db.session.commit()
        except:
            db.session.rollback()
            if throw_exception:
                raise
        finally:
            db.session.close()


class VenueRepository(BaseRepository):
    pass


class ShowRepository(BaseRepository):
    pass


class ArtistRepository(BaseRepository):
    pass
