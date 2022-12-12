'''
This file is part of soco.
'''
from utils import find_max, find_min, find_maxabs

class member_respoint():

    def __init__(self, id=None):
        self.number = None
        self.node = None
        #--
        self.unit_force = '[kip]'
        self.unit_moment = '[kip-ft]'
        #--
        self.res = []
        #--
        self.colLC = 1
        self.colFx = 3
        self.colFy = 4
        self.colFz = 5
        self.colMx = 6
        self.colMy = 7
        self.colMz = 8
        self.colMtot = 9
        self.colVtot = 10
        self.colboltmaxtension = 11
        self.colmaxboltcompression = 12
        self.colmaxboltshear = 13
        self.colFynorm = 14
        self.colFznorm = 15
    
    def calc_additional_forces(self):
        self.calc_Mtot()
        self.calc_Vtot()
        self.calc_bolt_maxtension()
        self.calc_bolt_maxcompression()
        self.calc_bolt_maxshear()
        self.calc_Fynorm()
        self.calc_Fznorm()
        
    #---
    def calc_Mtot(self):
        for record in self.res:
            My = record[self.colMy]
            Mz = record[self.colMz]
            record.append(round((My**2 + Mz**2)**0.5, 2))

    def calc_Vtot(self):
        for record in self.res:
            Fy = record[self.colFy]
            Fz = record[self.colFz]
            record.append(round((Fy**2 + Fz**2)**0.5, 2))

    def calc_bolt_maxtension(self):
        for record in self.res:
            My = abs(record[self.colMy])
            Mz = abs(record[self.colMz])
            Fx = record[self.colFx]
            #--
            if 'ft' in self.unit_moment: a = 1
            if 'in' in self.unit_moment: a = 12
            if 'm' in self.unit_moment: a = 0.305
            if 'mm' in self.unit_moment: a = 305
            #--   
            fp = Fx / 4
            fm = -My / a / 2 - Mz / a / 2
            f = fp + fm
            f = min(f,0)
            record.append(round(f, 2))

    def calc_bolt_maxcompression(self):
        for record in self.res:
            My = abs(record[self.colMy])
            Mz = abs(record[self.colMz])
            Fx = record[self.colFx]
            #--
            if 'ft' in self.unit_moment: a = 1
            if 'in' in self.unit_moment: a = 12
            if 'm' in self.unit_moment: a = 0.305
            if 'mm' in self.unit_moment: a = 305
            #--
            fp = Fx / 4
            fm = My / a / 2 + Mz / a / 2
            f = fp + fm
            f = max(f,0)
            record.append(round(f, 2))

    def calc_bolt_maxshear(self):
        for record in self.res:
            Fy = abs(record[self.colFy])
            Fz = abs(record[self.colFz])
            Mx = abs(record[self.colMx])
            fvy = Fy / 4
            fvz = Fz / 4
            #--
            if 'ft' in self.unit_moment: a = 1
            if 'in' in self.unit_moment: a = 12
            if 'm' in self.unit_moment: a = 0.305
            if 'mm' in self.unit_moment: a = 305
            #--
            fm = Mx / 2 / (a**2 + a**2)**0.5
            fmy = fm/2**0.5
            fmz = fm/2**0.5
            #--
            fy = fvy + fmy
            fz = fvz + fmz
            f =(fy**2 + fz**2)**0.5
            record.append(round(f, 2))

    def calc_Fynorm(self):
        for record in self.res:
            Fy = record[self.colFy]
            if 'i' in self.number:
                Fynom = Fy
            if 'j' in self.number:
                Fynom = -Fy
            record.append(Fynom)
            
    def calc_Fznorm(self):
        for record in self.res:
            Fz = record[self.colFz]
            if 'i' in self.number:
                Fznom = Fz
            if 'j' in self.number:
                Fznom = -Fz
            record.append(Fznom)
    #---
    @property
    def Fxmax(self):
        return find_max(self.res, self.colFx)
    @property
    def Fxmin(self):
        return find_min(self.res, self.colFx)


    @property
    def Fymaxabs(self):
        return find_maxabs(self.res, self.colFy)
        
    @property
    def Fzmaxabs(self):
        return find_maxabs(self.res, self.colFz)

    @property
    def Mxmaxabs(self):
        return find_maxabs(self.res, self.colMx)

    @property
    def Mymaxabs(self):
        return find_maxabs(self.res, self.colMy)
    @property
    def Mymax(self):
        return find_max(self.res, self.colMy)
    @property
    def Mymin(self):
        return find_min(self.res, self.colMy)

    @property
    def Mzmaxabs(self):
        return find_maxabs(self.res, self.colMz)
    @property
    def Mzmax(self):
        return find_max(self.res, self.colMz)
    @property
    def Mzmin(self):
        return find_min(self.res, self.colMz)

    @property
    def Mzmaxabs(self):
        return find_maxabs(self.res, self.colMz)
        
    @property
    def Mtotmax(self):
        return find_maxabs(self.res, self.colMtot)

    @property
    def Vtotmax(self):
        return find_maxabs(self.res, self.colVtot)

    @property
    def Bolttensionmax(self):
        return find_maxabs(self.res, self.colboltmaxtension)
        
    @property
    def Boltcompressionmax(self):
        return find_maxabs(self.res, self.colmaxboltcompression)

    @property
    def Boltshearmax(self):
        return find_maxabs(self.res, self.colmaxboltshear)     
        
    @property
    def Fynormmax(self):
        return find_max(self.res, self.colFynorm)
    @property
    def Fynormmin(self):
        return find_min(self.res, self.colFynorm)

    @property
    def Fznormmax(self):
        return find_max(self.res, self.colFznorm)
    @property
    def Fznormmin(self):
        return find_min(self.res, self.colFznorm)

    #---
    @property
    def Fxlist(self):
        return [i[self.colFx] for i in self.res]
    @property
    def Fylist(self):
        return [i[self.colFy] for i in self.res]
    @property
    def Fzlist(self):
        return [i[self.colFz] for i in self.res]
    @property
    def Mxlist(self):
        return [i[self.colMx] for i in self.res]
    @property
    def Mylist(self):
        return [i[self.colMy] for i in self.res]
    @property
    def Mzlist(self):
        return [i[self.colMz] for i in self.res]
        
    @property
    def Mtotlist(self):
        return [i[self.colMtot] for i in self.res]
    @property
    def Vtotlist(self):
        return [i[self.colVtot] for i in self.res]
        
    @property
    def MaxBoltmaxtensionlist(self):
        return [i[self.colboltmaxtension] for i in self.res]
    @property
    def Maxboltcompressionlist(self):
        return [i[self.colmaxboltcompression] for i in self.res] 
    @property
    def Maxboltshearlist(self):
        return [i[self.colmaxboltshear] for i in self.res]  
    
    @property
    def Fynormlist(self):
        return [i[self.colFynorm] for i in self.res]
    @property
    def Fznormlist(self):
        return [i[self.colFznorm] for i in self.res]

    @property
    def LClist(self):
        return [i[self.colLC] for i in self.res]
    @property
    def numberlist(self):
        return [self.number]*len(self.res)


#test if main
if __name__ == '__main__': 
    m = member_respoint()
    m.number = '2i'
    m.node = '1'
    #              L/C	Node     Fx     Fy      Fz    Mx  	 My 	Mz
    m.res.append(['1', '100', '9', 12.782, -0.283, 6.743, -0.003, 0,  4.299])
    m.res.append(['', '101', '9', 15.134, -53.945, 8.024, 0.014, 0, -239.807])
    m.calc_additional_forces()
    print(m.res[0])
    print(m.res[1])
    tab = []
    tab.append(['Member', 'LC', 'Node', 'Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz', 'Mtot', 'Vtot', 'boltmaxtension', 'boltcompression', 'maxboltshear',  'Fynorm',  'Fznorm'])
    tab.append(m.res[0])
    tab.append(m.res[1])
    from tabulate import tabulate
    print(m.number)
    print(tabulate(tab, headers="firstrow", tablefmt="grid"))
    print(m.Fynormmax)
    print(m.Fynormmin)
    print(m.Fznormmax)
    print(m.Fznormmin)
    print(m.Fynormlist)
    print(m.Fznormlist)
    print(m.Mymax)
    print(m.Mymin)
    

 
 
 
 
 
 
 
    