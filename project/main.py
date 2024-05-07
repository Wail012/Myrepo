from fastapi import FastAPI,Request,Form, Response,Depends
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from database import Base,engine,SessionLocal
from models import Employee,Groupe,Manager,ResponsableRH,Admin,Conge,Conge1,hday,nday,Congem,Congerh,Messagerh,Messagem
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Date
from datetime import date
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
app.g=0

@app.get("/")
async def read_root(request: Request):
   return templates.TemplateResponse("welcome.html", {"request": request})


@app.get("/ajoutemp",response_class=HTMLResponse)
async def read_root(request: Request):
    db = SessionLocal()
    g = db.query(Groupe).all()
    db.close()
    return templates.TemplateResponse("ajoutemp.html", {"request": request,"g":g})

@app.post("/ajoutemp",response_class=HTMLResponse)
def create_employee(request: Request,id: int = Form(...),nom: str = Form(...), prenom: str = Form(...), age: int = Form(...),groupe: int = Form(...),point: float = Form(...)):
    x=0
    db = SessionLocal()
    g = db.query(Groupe).all()
    e=db.query(Employee).filter_by(id=id).first()
    db.close()
    if e:
     x=1
    else:    
     employee = Employee(id=id,nom=nom, prenom=prenom, age=age,id_g=groupe,points=point)
     db = SessionLocal()
     db.add(employee)
     db.commit()
     db.refresh(employee)
     db.close()
     x=2
    

    return templates.TemplateResponse("ajoutemp.html", {"request": request,"g":g,"x":x})

@app.get("/modifemp1",response_class=HTMLResponse)
async def read_root(request: Request):
   x=0
   db = SessionLocal()
   e=db.query(Employee).all()
   db.close()
   return templates.TemplateResponse("modifemp1.html", {"request": request,"x":x,"e":e})

@app.post("/modifemp1",response_class=HTMLResponse,)
async def read_root(request: Request,id1: int = Form(...),db: Session = Depends(get_db)):
   x=0
   db = SessionLocal()
   e=db.query(Employee).filter_by(id=id1).first()
   db.close()
   if e:
      response = RedirectResponse(url="/modifemp2", status_code=303)
      response.set_cookie(key="my_cookie", value=int(id1))
      app.g=id1
      return RedirectResponse(url="/modifemp2", status_code=303)
   else:
      x=1
      return templates.TemplateResponse("modifemp1.html", {"request": request,"x":x})
    
@app.get("/modifemp2/{id1}",response_class=HTMLResponse)
async def read_root(request: Request,id1: int):
   x=0
   app.g=id1
   db = SessionLocal()
   g = db.query(Groupe).all()
   db.close()
   return templates.TemplateResponse("modifemp2.html", {"request": request,"x":x,"g":g})

@app.post("/modifemp2/4",response_class=HTMLResponse)
async def update_employee(
    request: Request,
    
    nom: str = Form(...),
    prenom: str = Form(...),
    age: int = Form(...),
    point: int = Form(...),
    ):
 db = SessionLocal()
 id2=int(app.g)
 e=db.query(Employee).get(id2)

 e.nom = nom
 e.prenom = prenom
 e.age = age
 e.points = point
 db.commit()
 db.close()
 db = SessionLocal()
 g = db.query(Groupe).all()
 db.close()
 x=1
 return templates.TemplateResponse("modifemp2.html", {"request": request,"x":x,"g":g})

@app.get("/suppemp1",response_class=HTMLResponse)
async def delete_employee(request: Request):
   x=0
   db = SessionLocal()
   e=db.query(Employee).all()
   db.close()
   return templates.TemplateResponse("suppemp1.html", {"request": request,"x":x,"e":e})

@app.get("/suppemp2/{id1}",response_class=HTMLResponse)
async def delete_employee(request: Request,id1: int):
   db = SessionLocal()
   e=db.query(Employee).get(id1)
   db.delete(e)
   db.commit()
   db.close()
   db = SessionLocal()
   e=db.query(Employee).all()
   db.close()

   return templates.TemplateResponse("suppemp1.html", {"request": request,"e":e})

@app.post("/suppemp1",response_class=HTMLResponse)
async def delete_employee(request: Request,id1: int = Form(...)):
   db = SessionLocal()
   e=db.query(Employee).get(id1)
   
   if e:
      db.delete(e)
      db.commit()
      db.close()
      x=2
   else:
      x=1
      db.close()
   return templates.TemplateResponse("suppemp1.html", {"request": request,"x":x})      


@app.get("/nmanager1",response_class=HTMLResponse)
async def nmanager(request: Request):
   db = SessionLocal()
   e=db.query(Groupe).all()
   db.close()
   return templates.TemplateResponse("nmanager1.html", {"request": request,"g":e})    

@app.post("/nmanager1",response_class=HTMLResponse)
async def nmanager(request: Request,groupe: int = Form(...)):
   db = SessionLocal()
   app.e1=db.query(Employee).filter_by(id_g=groupe)
   app.g1=groupe
   #app.e1=db.query(Employee).filter_by(id_g=groupe)
   return RedirectResponse(url="/nmanager2", status_code=303)

@app.get("/nmanager2",response_class=HTMLResponse)
async def nmanager(request: Request):
   x=0
   return templates.TemplateResponse("nmanager2.html", {"request": request,"g":app.e1,"x":x})    

@app.post("/nmanager2",response_class=HTMLResponse)
async def nmanager(request: Request,m: int = Form(...)):
   db = SessionLocal()
   e=db.query(Manager).filter_by(id_g=app.g1).first()
   if e:
    db.delete(e)
    
   b=db.query(Employee).get(m)
   b1=Manager(id=b.id,nom=b.nom,prenom=b.prenom,age=b.age,points=b.points,Salaire=b.Salaire,id_g=b.id_g)
   db.add(b1)
   db.commit()
   db.refresh(b1)
   db.close()
   x=1
   return templates.TemplateResponse("nmanager2.html", {"request": request,"g":app.e1,"x":x})


@app.get("/nrh1",response_class=HTMLResponse)
async def nmanager(request: Request):
   db = SessionLocal()
   e=db.query(Groupe).all()
   return templates.TemplateResponse("nrh1.html", {"request": request,"g":e})

@app.post("/nrh1",response_class=HTMLResponse)
async def nmanager(request: Request,groupe: int = Form(...)):

   app.g3=groupe
   return RedirectResponse(url="/nrh2", status_code=303)

@app.get("/nrh2",response_class=HTMLResponse)
async def nmanager(request: Request):
   x=0
   db = SessionLocal()
   e=db.query(Employee).all()
   db.close()
   return templates.TemplateResponse("nrh2.html", {"request": request,"g":e,"x":x})

@app.post("/nrh2",response_class=HTMLResponse)
async def nmanager(request: Request,g: int = Form(...)):
   db = SessionLocal()
   
   e4=db.query(ResponsableRH).get(g)
   db.close()
   if e4:
      pass
   else:
      db = SessionLocal()
      e5=db.query(Employee).get(g)
      e6=ResponsableRH(id=e5.id,nom=e5.nom,prenom=e5.prenom,age=e5.age)
      db.add(e6)
      db.commit()
      db.refresh(e6)
      db.close()
     
   db = SessionLocal()
   e=db.query(Employee).all()
   e3=db.query(Groupe).get(app.g3)
   e3.id_rh=g   
   db.commit()   
   db.close()
   db = SessionLocal()
   e=db.query(Employee).all()
   db.close()
   x=1
   return templates.TemplateResponse("nrh2.html", {"request": request,"g":e,"x":x})
   
@app.get("/suppmanager1",response_class=HTMLResponse)
async def nmanager(request: Request): 
   x=0
   db = SessionLocal()
   e=db.query(Manager).all()
   db.close()
   return templates.TemplateResponse("suppmanager1.html", {"request": request,"g":e,"x":x})

@app.post("/suppmanager1",response_class=HTMLResponse)
async def nmanager(request: Request,g1: int = Form(...)):
   db = SessionLocal()
   e=db.query(Manager).all()
   db.close()
   db = SessionLocal()
   e1=db.query(Manager).get(g1)
   db.delete(e1)
   db.commit()
   db.close()
   x=1
   return templates.TemplateResponse("suppmanager1.html", {"request": request,"g":e,"x":x})


@app.get("/supprh1",response_class=HTMLResponse)
async def nmanager(request: Request): 
   x=0
   db = SessionLocal()
   e=db.query(ResponsableRH).all()
   db.close()
   return templates.TemplateResponse("supprh1.html", {"request": request,"g":e,"x":x})

@app.post("/supprh1",response_class=HTMLResponse)
async def nmanager(request: Request,g1: int = Form(...)):
   db = SessionLocal()
   e=db.query(ResponsableRH).all()
   db.close()
   db = SessionLocal()
   e1=db.query(ResponsableRH).get(g1)
   
   db.delete(e1)
   db.commit()
   db.close()
   x=1
   return templates.TemplateResponse("supprh1.html", {"request": request,"g":e,"x":x})

@app.get("/login",response_class=HTMLResponse)
async def nmanager(request: Request):
   x=0
   return  templates.TemplateResponse("login.html", {"request": request,"x":x})


@app.post("/login",response_class=HTMLResponse)
async def nmanager(request: Request,id: int = Form(...),nom: str = Form(...)):
    db = SessionLocal()
    e4=db.query(Admin).get(id)
    db.close()
    e=db.query(ResponsableRH).get(id)
    db.close()
    db = SessionLocal()
    e1=db.query(Manager).get(id)
    db.close()
    db = SessionLocal()
    e2=db.query(Employee).get(id)
    db.close()
    if e4:
       app.user=id
       return  templates.TemplateResponse("welcomeadmin.html", {"request": request})
    if e:
       app.user=id
       return  templates.TemplateResponse("welcomerh.html", {"request": request})
    elif e1:
       app.user=id
       return  templates.TemplateResponse("welcomem.html", {"request": request})
    elif e2:
       app.user=id
       return  templates.TemplateResponse("empwelcome.html", {"request": request})
    else :
       x=1
       return  templates.TemplateResponse("login.html", {"request": request,"x":x})
    
import json



@app.get("/dconge",response_class=HTMLResponse)
async def nmanager(request: Request):
   x=0
   db = SessionLocal()
   e2=db.query(Employee).get(app.user)
   
   db.close()
   db = SessionLocal()
   e6=db.query(Employee).filter_by(id_g=e2.id_g)
   e7=[employe.to_dict() for employe in e6]
   e3=db.query(Conge).filter_by(approved="accepted")
   e4=db.query(Conge1).filter_by(id_g=e2.id_g)
   e5 = [conge.to_dict() for conge in e4]
   
   return  templates.TemplateResponse("dconge.html", {"request": request,"x":x,"e":e2,"c":e3,"c1":e5,"e7":e7})





@app.post("/dconge",response_class=HTMLResponse)
async def nmanager(request: Request,type1: str = Form(...),dated1: date = Form(...),datef1: date = Form(...)):

   
   db = SessionLocal()
   e2=db.query(Employee).get(app.user)
   e1=Conge(date_d=dated1,date_f=datef1,emp_id=app.user,approved="pending",type=type1,id_g=e2.id_g)
   db.add(e1)
   db.commit()
   db.refresh(e1)
   db.close()
   db = SessionLocal()
  
   e4=db.query(Conge1).all()
   e5 = [conge.to_dict() for conge in e4]
   e3=db.query(Conge).filter_by(approved="accepted")
   db.close()
   x=1
   return templates.TemplateResponse("dconge.html", {"request": request,"x":x,"e":e2,"c1":e5,"c":e3})

@app.get("/mconge",response_class=HTMLResponse)
async def nmanager(request: Request):
   x=0
   db = SessionLocal()
   e2=db.query(Employee).get(app.user)
   e1=db.query(Conge).filter_by(approved="pending",id_g=e2.id_g)
   

   db.close()
   return  templates.TemplateResponse("mconge.html", {"request": request,"x":x,"c":e1})

@app.get("/approve/{id1}",response_class=HTMLResponse)
async def nmanager(request: Request,id1: int):
   db = SessionLocal()
   e1=db.query(Conge).get(id1)
   e2=db.query(Employee).get(app.user)
   e6=Messagem(from1=e2.id,to=e1.emp_id,text1="demande de conge est approuve par le manager")
   db.add(e6)
   db.commit()
   db.refresh(e6)
   e1.approved="accepted"
   db.commit()
   db.close()
   db = SessionLocal()
   db.close()
   e1=db.query(Conge).filter_by(approved="pending")
   x=0
   return  templates.TemplateResponse("mconge.html", {"request": request,"x":x,"c":e1})


@app.get("/decline/{id1}",response_class=HTMLResponse)
async def nmanager(request: Request,id1: int):
   db = SessionLocal()
   e1=db.query(Conge).get(id1)
   e1.approved="declined"
   e2=db.query(Employee).get(app.user)
   e6=Messagem(from1=e2.id,to=e1.emp_id,text1="demande de conge est refuse par le manager")
   db.add(e6)
   db.commit()
   db.refresh(e6)
   db.commit()
   db.close()
   db = SessionLocal()
   db.close()
   e1=db.query(Conge).filter_by(approved="pending")
   x=0
   return  templates.TemplateResponse("mconge.html", {"request": request,"x":x,"c":e1})
   


@app.get("/rhconge",response_class=HTMLResponse)
async def nmanager(request: Request):
   x=0
   db = SessionLocal()
   e1=db.query(Conge).filter_by(approved="accepted")
   db.close()
   return  templates.TemplateResponse("rhconge.html", {"request": request,"x":x,"c":e1})


# @app.get("/approve1/{id1}",response_class=HTMLResponse)
# async def nmanager(request: Request,id1: int):
#    db = SessionLocal()
#    e1=db.query(Conge).get(id1)
#    e1.approved="accepted1"
   
#    emp=e1.emp_id
#    emp1=db.query(Employee).get(emp)
#    g=emp1.id_g
#    db.commit()
#    db.close()
   
#    # print (e1.date_d.month)
#    # print (e1.date_f.month)
#    for i in range(e1.date_d.month,e1.date_f.month+1):
#        if i == e1.date_d.month:
#           a=e1.date_d.day
#        else:
#           a=1
#        if i == e1.date_f.month:
#           b=e1.date_f.day 
#        else:
#           b=30

#        for j in range(a,b):
#         e2=Conge1(day=j,month=i,year=2023,emp_id=emp,id_g=g)
#         db = SessionLocal()
#         db.add(e2)
#         db.commit()
#         db.refresh(e2)
        

   
#    db = SessionLocal()
#    e6=db.query(Conge).filter_by(approved="accepted")
#    x=0
#    db.close()
#    return  templates.TemplateResponse("rhconge.html", {"request": request,"x":x,"c":e6})



@app.get("/approve1/{id1}", response_class=HTMLResponse)
async def nmanager(request: Request, id1: int):
    db = SessionLocal()
    e1 = db.query(Conge).get(id1)
    e1.approved = "accepted1"
    e2=db.query(Employee).get(app.user)
    e6=Messagerh(from1=e2.id,to=e1.emp_id,text1="demande de conge est approuve par le responsable rh")
    db.add(e6)
    db.commit()
    db.refresh(e6)
    emp = e1.emp_id
    emp1 = db.query(Employee).get(emp)
    g = emp1.id_g
    e5=db.query(hday).all()
    # Commit the changes to e1 before closing the session
    
    s=0
    
    for i in range(e1.date_d.month, e1.date_f.month + 1):
        if i == e1.date_d.month:
            a = e1.date_d.day
        else:
            a = 1
        if i == e1.date_f.month:
            b = e1.date_f.day+1
        else:
           if i == 1:
              b=32
           if i == 2:
              b=29
           if i == 3:
              b=32
           if i == 4:
              b=31
           if i == 5:
              b=32
           if i == 6:
              b=31
           if i == 7:
              b=32
           if i == 8:
              b=32
           if i == 9:
              b=31  
           if i == 10:
              b=32
           if i == 11:
              b=31
           if i == 8:
              b=32                               

        for j in range(a, b):
            e2 = Conge1(day=j, month=i, year=2023, emp_id=emp, id_g=g)
            m=1
            for k in range(1, 13):
              
              if k == 1:
               r=32
              if k == 2:
               r=29
              if k == 3:
               r=32
              if k == 4:
               r=31
              if k == 5:
               r=32
              if k == 6:
               r=31
              if k == 7:
               r=32
              if k == 8:
               r=32
              if k == 9:
               r=31  
              if k == 10:
               r=32
              if k == 11:
               r=31
              if k == 8:
               r=32  
              for l in range(1, r):
               if (m != 1 and m != 7) and j == l and i == k :
                  s=s+1
                  for p in e5:
                     if p.day == j and p.month == i:
                        s=s-1
               if m == 7:
                  m=0
               m=m+1      
                   
            # Use the same session for adding e2 and committing changes
            db.add(e2)
            db.commit()
            db.refresh(e2)

    e6 = db.query(Conge).filter_by(approved="accepted")
    x = 0
    db.close()
    db = SessionLocal()
    e1 = db.query(Conge).get(id1)
    

    emp = e1.emp_id
    emp1 = db.query(Employee).get(emp)
    
    emp1.points=emp1.points-s
    db.commit()
    db.close()
    return templates.TemplateResponse("rhconge.html", {"request": request, "x": x, "c": e6})



# @app.get("/approve1/{id1}", response_class=HTMLResponse)
# async def nmanager(request: Request, id1: int):
#     db = SessionLocal()
#     e1 = db.query(Conge).get(id1)
#     e1.approved = "accepted1"

#     emp = e1.emp_id
#     emp1 = db.query(Employee).get(emp)
#     g = emp1.id_g
#     e2 = db.query(Conge1).filter_by(emp_id=g)
#     # Commit the changes to e1 before closing the session
    

#     for i in range(e1.date_d.month, e1.date_f.month + 1):
#         if i == e1.date_d.month:
#             a = e1.date_d.day
#         else:
#             a = 1
#         if i == e1.date_f.month:
#             b = e1.date_f.day+1
#         else:
#             b = 30
#         e3=db.query(Conge1).filter_by(id_g=g,month=i)
#         for j in e3:
#             e4 = db.query(Conge1).filter_by(id_g=g,month=i)

#             # Use the same session for adding e2 and committing changes
#             db.add(e2)
#             db.commit()
#             db.refresh(e2)

#     e6 = db.query(Conge).filter_by(approved="accepted")
#     x = 0
#     db.close()

#     return templates.TemplateResponse("rhconge.html", {"request": request, "x": x, "c": e6})




@app.get("/decline1/{id1}",response_class=HTMLResponse)
async def nmanager(request: Request,id1: int):
   db = SessionLocal()
   e1=db.query(Conge).get(id1)
   e1.approved="declined1"
   e2=db.query(Employee).get(app.user)
   e6=Messagerh(from1=e2.id,to=e1.emp_id,text1="demande de conge est refuse par le responsable rh")
   db.add(e6)
   db.commit()
   db.refresh(e6)
   db.commit()
   db.close()
   db = SessionLocal()
   db.close()
   e1=db.query(Conge).filter_by(approved="accepted")
   x=0
   return  templates.TemplateResponse("rhconge.html", {"request": request,"x":x,"c":e1})

@app.get("/pemp",response_class=HTMLResponse)
async def nmanager(request: Request):
 db = SessionLocal()
 e1=db.query(Employee).get(app.user)
 

 return  templates.TemplateResponse("demp.html", {"request": request,"u":e1})

@app.get("/home",response_class=HTMLResponse)
async def nmanager(request: Request):
   return  templates.TemplateResponse("welcome.html", {"request": request})



@app.get("/dconge1",response_class=HTMLResponse)
async def nmanager(request: Request):
      x=0
      db = SessionLocal()
      e1=db.query(Employee).get(app.user)
      return  templates.TemplateResponse("dconge1.html", {"request": request,'e':e1,'x':x})

@app.post("/dconge1",response_class=HTMLResponse)
async def nmanager(request: Request,type1: str = Form(...),dated1: date = Form(...),datef1: date = Form(...)):
   
   
   db = SessionLocal()
   e1=db.query(Employee).get(app.user)
   e8=db.query(nday).all()
   e2=Conge(date_d=dated1,date_f=datef1,emp_id=app.user,approved="pending",type=type1,id_g=e1.id_g)
   n=0
   for i in range(e2.date_d.month, e2.date_f.month + 1):
        if i == e2.date_d.month:
            a = e2.date_d.day
        else:
            a = 1
        if i == e2.date_f.month:
            b = e2.date_f.day+1
        else:
           if i == 1:
              b=32
           if i == 2:
              b=29
           if i == 3:
              b=32
           if i == 4:
              b=31
           if i == 5:
              b=32
           if i == 6:
              b=31
           if i == 7:
              b=32
           if i == 8:
              b=32
           if i == 9:
              b=31  
           if i == 10:
              b=32
           if i == 11:
              b=31
           if i == 8:
              b=32                               

        for j in range(a, b):
           for k in e8:
              if j == k.day and i == k.month :
                 n=1
           

   if n == 0:
    db.add(e2)
    db.commit()
    db.refresh(e2)
    db.close()
    p=0
   else :
    p=1
   db = SessionLocal()
   e1=db.query(Employee).get(app.user)
   db.close()
   x=1
   return  templates.TemplateResponse("dconge1.html", {"request": request,'e':e1,'x':x,'p':p})

@app.get("/hday1",response_class=HTMLResponse)
async def nmanager(request: Request):
      x=0
      db = SessionLocal()
      e1=db.query(hday).all()
      return  templates.TemplateResponse("hday1.html", {"request": request,'e':e1,'x':x})

@app.post("/hday1",response_class=HTMLResponse)
async def nmanager(request: Request, type1: str = Form(...),dated1: date = Form(...)):
      x=1
      db = SessionLocal()
      e2=hday(type=type1,day=dated1.day,month=dated1.month)
      db.add(e2)
      db.commit()
      db.refresh(e2)
      
      e1=db.query(hday).all()
      db.close()
      x=1
      return  templates.TemplateResponse("hday1.html", {"request": request,'e':e1,'x':x})

@app.get("/supphday/{id1}",response_class=HTMLResponse)
async def nmanager(request: Request,id1: int):
      x=0
      db = SessionLocal()
      e2=db.query(hday).get(id1)
      db.delete(e2)
      db.commit()
      e1=db.query(hday).all()
      db.close()
      return  templates.TemplateResponse("hday1.html", {"request": request,'e':e1,'x':x})


@app.get("/nday1",response_class=HTMLResponse)
async def nmanager(request: Request):
      x=0
      db = SessionLocal()
      e1=db.query(nday).all()
      return  templates.TemplateResponse("nday1.html", {"request": request,'e':e1,'x':x})



@app.post("/nday1",response_class=HTMLResponse)
async def nmanager(request: Request, type1: str = Form(...),dated1: date = Form(...)):
      x=1
      db = SessionLocal()
      e2=nday(type=type1,day=dated1.day,month=dated1.month)
      db.add(e2)
      db.commit()
      db.refresh(e2)
      
      e1=db.query(nday).all()
      db.close()
      x=1
      return  templates.TemplateResponse("nday1.html", {"request": request,'e':e1,'x':x})



@app.get("/suppnday/{id1}",response_class=HTMLResponse)
async def nmanager(request: Request,id1: int):
      x=0
      db = SessionLocal()
      e2=db.query(nday).get(id1)
      db.delete(e2)
      db.commit()
      e1=db.query(nday).all()
      db.close()
      return  templates.TemplateResponse("nday1.html", {"request": request,'e':e1,'x':x})


@app.get("/mconge2",response_class=HTMLResponse)
async def nmanager(request: Request):
      x=2
      db = SessionLocal()
      e4=db.query(Employee).get(app.user)
      e3=db.query(Congem).all()
      
      e2=db.query(Conge).filter_by(approved="pending",id_g=e4.id_g)
      e5=db.query(Conge).filter_by(approved="accepted1" ,id_g=e4.id_g)
      e9=db.query(Conge).filter_by(approved="accepted" ,id_g=e4.id_g)
      e6=db.query(Employee).filter_by(id_g=e4.id_g)
      s=0
      
      for i in e6:
       for j in e5:
          if i.id == j.emp_id:
             s=s+1
             break
       
      if s < 2:
            e5=db.query(Conge).filter_by(approved="pending" ,id_g=e4.id_g)
            s1=0
            for p in e5:
               s1=s1+1
            while s < 2 and s1 !=0 :
               for j in e2:
                  if s < 2:
                   if j.type == "maladie":
                      j.approved = "accepted"
                      
                      e7=Congem(date_d=j.date_d,date_f=j.date_f,emp_id=j.emp_id,approved=j.approved,type=j.type,id_g=j.id_g)
                      db.add(e7)
                      db.commit()
                      db.refresh(e7)
                      
                      s=s+1

               if s < 2:
                for j in e2:
                  if s < 2:
                   if j.type == "formation":
                      j.approved = "accepted"
                      
                      e7=Congem(date_d=j.date_d,date_f=j.date_f,emp_id=j.emp_id,approved=j.approved,type=j.type,id_g=j.id_g)
                      db.add(e7)
                      db.commit()
                      db.refresh(e7)
                      
                      s=s+1

               if s < 2:
                for j in e2:
                  if s < 2:
                   if j.type == "vacances":
                      j.approved = "accepted"
                      
                      e7=Congem(date_d=j.date_d,date_f=j.date_f,emp_id=j.emp_id,approved=j.approved,type=j.type,id_g=j.id_g)
                      db.add(e7)
                      db.commit()
                      db.refresh(e7)
                      
                      s=s+1  


               e5=db.query(Conge).filter_by(approved="pending" ,id_g=e4.id_g)
               s1=0
               for p in e5:
                s1=s1+1



      e2=db.query(Conge).filter_by(approved="pending",id_g=e4.id_g)
      for i in e2:
         i.approved="declined"
         e7=Congem(date_d=i.date_d,date_f=i.date_f,emp_id=i.emp_id,approved=i.approved,type=i.type,id_g=i.id_g)
         db.add(e7)
         db.commit()
      e3=db.query(Congem).all()
      db.close()
      return  templates.TemplateResponse("mconge.html", {"request": request,'c':e2,'x':x,'e3':e3})


@app.get("/rhconge2",response_class=HTMLResponse)
async def nmanager(request: Request):

   
   x=2
   db = SessionLocal()
   e2=db.query(Conge).filter_by(approved="accepted1")
   e11=db.query(hday).all()
   e3=db.query(Groupe).all()

   for i in e3:
      e4= db.query(Employee).filter_by(id_g=i.id)
      s=0
      for j in e4:
         for k in e2:
            if k.emp_id == j.id:
               s=s+1
               break

      if s<2:
       e8=db.query(Conge).filter_by(approved="accepted",id_g=i.id)
       s1=0
       for p in e8:
          s1=s1+1

       while s < 2 and s1 != 0:
               for j in e8:
                  if s < 2:
                   if j.type == "maladie":
                      j.approved = "accepted1"
                      
                      e7=Congerh(date_d=j.date_d,date_f=j.date_f,emp_id=j.emp_id,approved=j.approved,type=j.type,id_g=j.id_g)
                      s2=0
                      db.add(e7)
                      db.commit()
                      db.refresh(e7)
                      
                      s=s+1
                      for p in range(j.date_d.month, j.date_f.month + 1):
                       if p == j.date_d.month:
                        a = j.date_d.day
                       else:
                        a = 1
                       if p == j.date_f.month:
                        b = j.date_f.day+1
                       else:
                        if p == 1:
                         b=32
                        if p == 2:
                         b=29
                        if p == 3:
                         b=32
                        if p == 4:
                         b=31
                        if p == 5:
                         b=32
                        if p == 6:
                         b=31
                        if p == 7:
                         b=32
                        if p == 8:
                         b=32
                        if p == 9:
                         b=31  
                        if p == 10:
                         b=32
                       if p == 11:
                        b=31
                       if i == 8:
                        b=32                               

                       for e in range(a, b):
                        e12 = Conge1(day=e, month=p, year=2023, emp_id=j.emp_id, id_g=j.id_g)
                        m=1
                        for v in range(1, 13):
              
                         if v == 1:
                          r=32
                         if v == 2:
                          r=29
                         if v == 3:
                          r=32
                         if v == 4:
                          r=31
                         if v == 5:
                          r=32
                         if v == 6:
                          r=31
                         if v == 7:
                          r=32
                         if v == 8:
                          r=32
                         if v == 9:
                          r=31  
                         if v == 10:
                          r=32
                         if v == 11:
                          r=31
                         if v == 8:
                          r=32  
                         for l in range(1, r):
                          if (m != 1 and m != 7) and e == l and p == v :
                           s2=s2+1
                           for n in e11:
                            if n.day == e and n.month == p:
                             s2=s2-1
                          if m == 7:
                           m=0
                          m=m+1      
                      
            # Use the same session for adding e2 and committing changes
                        db.add(e12)
                        db.commit()
                        db.refresh(e12)
                      e13=db.query(Employee).get(j.emp_id)
                      e13.points=e13.points-s2
                      db.commit()
               if s < 2:
                for j in e8:
                  if s < 2:
                   if j.type == "formation":
                      j.approved = "accepted1"
                      s2=0
                      e7=Congerh(date_d=j.date_d,date_f=j.date_f,emp_id=j.emp_id,approved=j.approved,type=j.type,id_g=j.id_g)
                      db.add(e7)
                      db.commit()
                      db.refresh(e7)
                      
                      s=s+1
                      for p in range(j.date_d.month, j.date_f.month + 1):
                       if p == j.date_d.month:
                        a = j.date_d.day
                       else:
                        a = 1
                       if p == j.date_f.month:
                        b = j.date_f.day+1
                       else:
                        if p == 1:
                         b=32
                        if p == 2:
                         b=29
                        if p == 3:
                         b=32
                        if p == 4:
                         b=31
                        if p == 5:
                         b=32
                        if p == 6:
                         b=31
                        if p == 7:
                         b=32
                        if p == 8:
                         b=32
                        if p == 9:
                         b=31  
                        if p == 10:
                         b=32
                       if p == 11:
                        b=31
                       if i == 8:
                        b=32                               

                       for e in range(a, b):
                        e12 = Conge1(day=e, month=p, year=2023, emp_id=j.emp_id, id_g=j.id_g)
                        m=1
                        for v in range(1, 13):
              
                         if v == 1:
                          r=32
                         if v == 2:
                          r=29
                         if v == 3:
                          r=32
                         if v == 4:
                          r=31
                         if v == 5:
                          r=32
                         if v == 6:
                          r=31
                         if v == 7:
                          r=32
                         if v == 8:
                          r=32
                         if v == 9:
                          r=31  
                         if v == 10:
                          r=32
                         if v == 11:
                          r=31
                         if v == 8:
                          r=32  
                         for l in range(1, r):
                          if (m != 1 and m != 7) and e == l and p == v :
                           s2=s2+1
                           for n in e11:
                            if n.day == e and n.month == p:
                             s2=s2-1
                          if m == 7:
                           m=0
                          m=m+1 


                        db.add(e12)
                        db.commit()
                        db.refresh(e12)
                      e13=db.query(Employee).get(j.emp_id)
                      e13.points=e13.points-s2
                      db.commit()
               if s < 2:
                for j in e8:
                  if s < 2:
                   if j.type == "vacances":
                      j.approved = "accepted1"
                      s2=0
                      e7=Congerh(date_d=j.date_d,date_f=j.date_f,emp_id=j.emp_id,approved=j.approved,type=j.type,id_g=j.id_g)
                      db.add(e7)
                      db.commit()
                      db.refresh(e7)
                      
                      s=s+1
                      for p in range(j.date_d.month, j.date_f.month + 1):
                       if p == j.date_d.month:
                        a = j.date_d.day
                       else:
                        a = 1
                       if p == j.date_f.month:
                        b = j.date_f.day+1
                       else:
                        if p == 1:
                         b=32
                        if p == 2:
                         b=29
                        if p == 3:
                         b=32
                        if p == 4:
                         b=31
                        if p == 5:
                         b=32
                        if p == 6:
                         b=31
                        if p == 7:
                         b=32
                        if p == 8:
                         b=32
                        if p == 9:
                         b=31  
                        if p == 10:
                         b=32
                       if p == 11:
                        b=31
                       if i == 8:
                        b=32                               

                       for e in range(a, b):
                        e12 = Conge1(day=e, month=p, year=2023, emp_id=j.emp_id, id_g=j.id_g)
                        m=1
                        for v in range(1, 13):
              
                         if v == 1:
                          r=32
                         if v == 2:
                          r=29
                         if v == 3:
                          r=32
                         if v == 4:
                          r=31
                         if v == 5:
                          r=32
                         if v == 6:
                          r=31
                         if v == 7:
                          r=32
                         if v == 8:
                          r=32
                         if v == 9:
                          r=31  
                         if v == 10:
                          r=32
                         if v == 11:
                          r=31
                         if v == 8:
                          r=32  
                         for l in range(1, r):
                          if (m != 1 and m != 7) and e == l and p == v :
                           s2=s2+1
                           for n in e11:
                            if n.day == e and n.month == p:
                             s2=s2-1
                          if m == 7:
                           m=0
                          m=m+1 


                        db.add(e12)
                        db.commit()
                        db.refresh(e12)

                      e13=db.query(Employee).get(j.emp_id)
                      e13.points=e13.points-s2
                      db.commit()
               e8=db.query(Conge).filter_by(approved="accepted",id_g=i.id)
               s1=0
               for p in e8:
                s1=s1+1

   e5=db.query(Conge).filter_by(approved="accepted")

   for i in e5:
      i.approved = "declined"
      e7=Congerh(date_d=i.date_d,date_f=i.date_f,emp_id=i.emp_id,approved=i.approved,type=i.type,id_g=i.id_g)
      db.add(e7)
      db.commit()
      db.refresh(e7)
   e3=db.query(Congerh).all()
   db.close()
   return  templates.TemplateResponse("rhconge.html", {"request": request,'c':e5,'x':x,'e3':e3})




@app.get("/dcongerh",response_class=HTMLResponse)
async def nmanager(request: Request):
     x=0
     db = SessionLocal()
     e8=db.query(Groupe).all()
     e2=db.query(Employee).get(app.user)
   
     db.close()
     db = SessionLocal()
     e6=db.query(Employee).filter_by(id_g=e2.id_g)
     e7=[employe.to_dict() for employe in e6]
     e3=db.query(Conge).filter_by(approved="accepted")
     e4=db.query(Conge1).filter_by(id_g=e2.id_g)
     e5 = [conge.to_dict() for conge in e4]
   
     return  templates.TemplateResponse("dcongerh.html", {"request": request,"x":x,"e":e2,"c":e3,"c1":e5,"e7":e7,'g':e8})
   



@app.post("/dcongerh",response_class=HTMLResponse)
async def nmanager(request: Request,id1: int = Form(...)):
     x=1
     db = SessionLocal()
     
     e8=db.query(Groupe).all()
     e2=db.query(Employee).get(app.user)
   
     db.close()
     db = SessionLocal()
     e6=db.query(Employee).filter_by(id_g=e2.id_g)
     e7=[employe.to_dict() for employe in e6]
     e3=db.query(Conge).filter_by(approved="accepted")
     e4=db.query(Conge1).filter_by(id_g=id1)
     e5 = [conge.to_dict() for conge in e4]
   
     return  templates.TemplateResponse("dcongerh.html", {"request": request,"x":x,"e":e2,"c":e3,"c1":e5,"e7":e7,'g':e8})

@app.get("/message",response_class=HTMLResponse)
async def nmanager(request: Request):
  
  db = SessionLocal()
  e2=db.query(Employee).get(app.user)
  e1=db.query(Messagem).filter_by(to=e2.id)
  e3=db.query(Messagerh).filter_by(to=e2.id)
    
  return  templates.TemplateResponse("message.html", {"request": request,"mrh":e3,"m":e1})


