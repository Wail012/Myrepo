# from sqlalchemy import  Column, Integer, String, Float, Date,ForeignKey
# from database import Base
# from sqlalchemy.orm import relationship


# class responsablerh(Base):
#     __tablename__ = "responsablerh"

#     id = Column(Integer, primary_key=True)
#     nom = Column(String)
#     prenom=Column(String)
#     age = Column(Integer)
#     g_rh = relationship("groupe", back_populates="responsable_rh")



# class groupe(Base):
#     __tablename__ = "groupe"

#     id = Column(Integer, primary_key=True)
#     specialite = Column(String)
#     nb_emp=Column(Integer)
#     id_rh= Column(Integer, ForeignKey("responsablerh.id"))     
#     responsable_rh = relationship("responsablerh", back_populates="g_rh")
#     eg1 = relationship("employee", back_populates="eg2")
#     mg2=relationship("manager", back_populates="mg1") 


# class employee(Base):
#     __tablename__ = "employees"

#     id = Column(Integer, primary_key=True)
#     nom = Column(String)
#     prenom=Column(String)
#     age = Column(Integer)
#     Salaire=Column(Float)
#     points=Column(Float)
#     id_g= Column(Integer, ForeignKey("groupe.id")) 
#     eg2 = relationship("groupe", back_populates="eg1")
#     ec1 = relationship("conge", back_populates="ec2")

# class conge(Base):
#     __tablename__ = "conge"

#     id = Column(Integer, primary_key=True)
#     date_d = Column(Date)
#     date_f=Column(Date)
#     emp_id= Column(Integer, ForeignKey("employees.id"))
#     ec2 = relationship("employee", back_populates="ec1")


# class manager(Base):
#     __tablename__ = "manager"

#     id = Column(Integer, primary_key=True)
#     nom = Column(String)
#     prenom=Column(String)
#     age = Column(Integer)
#     Salaire=Column(Float)
#     points=Column(Float)
#     id_g= Column(Integer, ForeignKey("groupe.id"))

#     mg1=relationship("groupe", back_populates="mg2")   
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ResponsableRH(Base):
    __tablename__ = "responsablerh"

    id = Column(Integer, primary_key=True)
    nom = Column(String)
    prenom = Column(String)
    age = Column(Integer)
    groupes = relationship("Groupe", back_populates="responsable_rh")
    messagerh=relationship("Messagerh", back_populates="rh2")

class Groupe(Base):
    __tablename__ = "groupe"

    id = Column(Integer, primary_key=True)
    specialite = Column(String)
    
    id_rh = Column(Integer, ForeignKey("responsablerh.id"))
    responsable_rh = relationship("ResponsableRH", back_populates="groupes")
    employees = relationship("Employee", back_populates="groupe")
    managers = relationship("Manager", back_populates="groupe")
    conges1 = relationship("Conge1", back_populates="groupe")
    conge = relationship("Conge", back_populates="groupe")
    congem = relationship("Congem", back_populates="groupe1")
    congerh = relationship("Congerh", back_populates="groupe2")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    nom = Column(String)
    prenom = Column(String)
    age = Column(Integer)
    Salaire = Column(Float)
    points = Column(Float)
    id_g = Column(Integer, ForeignKey("groupe.id"))
    groupe = relationship("Groupe", back_populates="employees")
    conges = relationship("Conge", back_populates="employee")
    conge1 = relationship("Conge1", back_populates="employee")
    congesm = relationship("Congem", back_populates="employee1")
    congesrh = relationship("Congerh", back_populates="employee2")
    messagerh= relationship("Messagerh", back_populates="employee3")
    messagem=relationship("Messagem", back_populates="employee4")
    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "prenom": self.prenom,
            "age": self.age,
            "Salaire": self.Salaire,
            "points": self.points,
            "id_g": self.id_g,
        }

class Conge(Base):
    __tablename__ = "conge"

    id = Column(Integer, primary_key=True,index=True)
    date_d = Column(Date)
    date_f = Column(Date)
    emp_id = Column(Integer, ForeignKey("employees.id"))
    approved = Column(String)
    type = Column(String)
    employee = relationship("Employee", back_populates="conges")
    id_g = Column(Integer, ForeignKey("groupe.id"))
    groupe = relationship("Groupe", back_populates="conge")

class Congem(Base):
    __tablename__ = "congem"

    id = Column(Integer, primary_key=True,index=True)
    date_d = Column(Date)
    date_f = Column(Date)
    emp_id = Column(Integer, ForeignKey("employees.id"))
    approved = Column(String)
    type = Column(String)
    employee1 = relationship("Employee", back_populates="congesm")
    id_g = Column(Integer, ForeignKey("groupe.id"))
    groupe1 = relationship("Groupe", back_populates="congem")




class Congerh(Base):
    __tablename__ = "congerh"

    id = Column(Integer, primary_key=True,index=True)
    date_d = Column(Date)
    date_f = Column(Date)
    emp_id = Column(Integer, ForeignKey("employees.id"))
    approved = Column(String)
    type = Column(String)
    employee2 = relationship("Employee", back_populates="congesrh")
    id_g = Column(Integer, ForeignKey("groupe.id"))
    groupe2 = relationship("Groupe", back_populates="congerh")


class Manager(Base):
    __tablename__ = "manager"

    id = Column(Integer, primary_key=True)
    nom = Column(String)
    prenom = Column(String)
    age = Column(Integer)
    Salaire = Column(Float)
    points = Column(Float)
    id_g = Column(Integer, ForeignKey("groupe.id"))
    groupe = relationship("Groupe", back_populates="managers")
    messagem=relationship("Messagem", back_populates="m2")
class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True)
    nom = Column(String)
   
   
class Conge1(Base):
        __tablename__ = "Conge1"
        id = Column(Integer, primary_key=True)
        day= Column(Integer)
        month= Column(Integer)
        year= Column(Integer)
        emp_id = Column(Integer, ForeignKey("employees.id"))
        status = Column(Integer)
        id_g = Column(Integer, ForeignKey("groupe.id"))
        groupe = relationship("Groupe", back_populates="conges1")
        employee = relationship("Employee", back_populates="conge1")

        def to_dict(self):
         return {
            "id": self.id,
            "day": self.day,
            "month": self.month,
            "year": self.year,
            "emp_id": self.emp_id,
            "status": self.status,
            "id_g": self.id_g,
        }

class hday(Base):
        __tablename__ = "hdays"
        id = Column(Integer, primary_key=True)
        day= Column(Integer)
        month= Column(Integer)
        type = Column(String)


class nday(Base):
        __tablename__ = "ndays"
        id = Column(Integer, primary_key=True)
        day= Column(Integer)
        month= Column(Integer)
        type = Column(String)        


class Messagerh(Base):
        __tablename__ = "messsagerh"
        id = Column(Integer, primary_key=True)
        from1 = Column(Integer, ForeignKey("responsablerh.id"))
        to= Column(Integer, ForeignKey("employees.id"))
        text1 = Column(String)                
        employee3 = relationship("Employee", back_populates="messagerh")
        rh2=relationship("ResponsableRH", back_populates="messagerh")



class Messagem(Base):
        __tablename__ = "messsagem"
        id = Column(Integer, primary_key=True)
        from1 = Column(Integer, ForeignKey("manager.id"))
        to= Column(Integer, ForeignKey("employees.id"))
        text1 = Column(String)                
        employee4 = relationship("Employee", back_populates="messagem")
        m2=relationship("Manager", back_populates="messagem")        