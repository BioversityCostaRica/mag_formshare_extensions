from formshare.models.meta import Base
from sqlalchemy import Column, Unicode, DECIMAL


class CNECrops(Base):
    __tablename__ = "cne_cultivos"

    Nombre = Column(Unicode(120), primary_key=True)
    i_p_arrasada = Column(DECIMAL(6, 2))
    i_p_anegada = Column(DECIMAL(6, 2))
    i_p_volcamiento = Column(DECIMAL(6, 2))
    i_p_excesolluvia = Column(DECIMAL(6, 2))
    i_c_arrasada = Column(DECIMAL(6, 2))
    i_c_anegado = Column(DECIMAL(6, 2))
    i_c_volcamiento = Column(DECIMAL(6, 2))
    i_c_excesolluvia = Column(DECIMAL(6, 2))
    costoestablecimiento = Column(DECIMAL(11, 2))
    costocosecha = Column(DECIMAL(11, 2))
    cantidadunidades = Column(DECIMAL(8, 2))


class CNELivestock(Base):
    __tablename__ = "cne_pecuario"

    actividad = Column(Unicode(120), primary_key=True)
    costo = Column(DECIMAL(11, 2))
