import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, Table
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from typing import List
from eralchemy2 import render_er

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    email = Column(String(80), unique=True)

    carrito_id = Column(Integer, ForeignKey("shoppingcart.id"))
    carrito = relationship("ShoppingCart", backref="user")


class Address(Base):
    __tablename__ = 'address'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False)
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship(Person)

    def to_dict(self):
        return {}


categories_association_table = Table(
    "categories_association_table",
    Base.metadata,
    Column("product_id", ForeignKey("products.id"), primary_key=True),
    Column("categories_id", ForeignKey("categories.id"), primary_key=True),
    # products
)

class Categoria(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column(String(80), nullable=False)
    productos : Mapped[List['Products']] = relationship(secondary=categories_association_table, back_populates="categories")

class Products(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column(String(80), nullable=False, unique=False)
    description = Column(String(1024), nullable=True)
    precio = Column(Numeric(2), nullable=False)
    categorias : Mapped[List['Categoria']] = relationship(secondary=categories_association_table, back_populates="products")

class ShoppingCart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True)
    # user_id = Column(Integer, ForeignKey("person.id"))
    # user = relationship("Person", backref="carrito")
    # productos_id = Column(Integer, ForeignKey("products.id"))
    # productos = relationship("Productos", backref="likes")


## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
