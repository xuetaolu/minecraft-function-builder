from api_motion import *

class FallingBlock:
  def __init__(self):
    self.type = 'fallingBlock'
    self.g, self.f = getGFByType(self.type)

  def getMotionBy2PWithT(self, x,y,z, X,Y,Z, t, gravity=True):
    vx = getV0BySt(     0, self.f, X-x, t)
    vz = getV0BySt(     0, self.f, Z-z, t)
    if gravity:
      vy = getV0BySt(self.g, self.f, Y-y, t)
    else:
      vy = getV0BySt(     0, self.f, Y-y, t)

    if abs(vx) > 10 or abs(vy) > 10 or abs(vz) > 10:
      print(f'[Error]: Motion > 10.0 ! [{vx}, {vy}, {vz}]')
      return 0.0,0.0,0.0
    else:
      return vx, vy, vz

  def getCmdBy2PWithT(self, x,y,z, X,Y,Z, t, gravity=True, block='wool', data='0', toSet=False):
    vx, vy, vz = self.getMotionBy2PWithT(x,y,z, X,Y,Z, t, gravity)
    if abs(vx) > 10 or abs(vy) > 10 or abs(vz) > 10:
      print(f'[Error]: Motion > 10.0 ! [{vx}, {vy}, {vz}] in getCmdBy2PWithT')
      return ''
    else:
      time = 600-t if toSet else 600+1-t
      noGravity = 0 if gravity else 1
      return f'summon falling_block {x} {y} {z} {{Motion:[{vx},{vy},{vz}],DropItem:0b,Time:{time},Block:"{block}",Data:{data},NoGravity:{noGravity}}}'

  def getMotionTBy2PWithTop(self, x,y,z, X,Y,Z, top):
    # # New method
    t = getTByStWithTop(self.g,self.f, Y-y, top-y)
    t = round(t)
    vy = getV0BySt(self.g,self.f, Y-y, t)
    vx = getV0BySt(     0,self.f, X-x, t)
    vz = getV0BySt(     0,self.f, Z-z, t)
    return (vx,vy,vz), t
    # gravity=True
    # # Old method
    # up, down = top-y, top-Y
    # t0 = getUpTBySt(self.g,self.f, up)
    # t1 = getDownTBySt(self.g,self.f, down)
    # t  = round(t1-t0)
    # # t = int(t1-t0)
    # vy = getV0BySt(self.g,self.f, Y-y, t)
    # # vy = getVtByV0(self.g,self.f, 0.0, t0)
    # vx = getV0BySt(     0,self.f, X-x, t)
    # vz = getV0BySt(     0,self.f, Z-z, t)
    # return (vx,vy,vz), t

  def getCmdTBy2PWithTop(self, x,y,z, X,Y,Z, top, block='wool', data='0', toSet=False):
    motion, t = self.getMotionTBy2PWithTop(x,y,z, X,Y,Z, top)
    vx,vy,vz  = motion
    if abs(vx) > 10 or abs(vy) > 10 or abs(vz) > 10:
      print(f'[Error]: Motion > 10.0 ! [{vx}, {vy}, {vz}] in getCmdTBy2PWithTop')
      return '', 0
    else:
      time = 600-int(t) if toSet else 600+1-t
      return f'summon falling_block {x} {y} {z} {{Motion:[{vx},{vy},{vz}],DropItem:0b,Time:{time},Block:"{block}",Data:{data},NoGravity:0}}', int(t)



  def getPosBy1PWithV0(self, x,y,z, vx, vy, vz, t, gravity=True):
    dx = getStByV0(     0, self.f, vx, t)
    dz = getStByV0(     0, self.f, vz, t)
    if gravity:
      dy = getStByV0(self.g, self.f, vy, t)
    else:
      dy = getStByV0(     0, self.f, vy, t)

    return x+dx, y+dy, z+dz

  def getMotionByV0WithT(self, vx,vy,vz, t, gravity=True):
    vx = getVtByV0(     0, self.f, vx, t)
    vz = getVtByV0(     0, self.f, vz, t)
    if gravity:
      vy = getVtByV0(self.g, self.f, vy, t)
    else:
      vy = getVtByV0(     0, self.f, vy, t)

    return vx, vy, vz

  def getHushCmdsBy2PWithT(self, x,y,z, X,Y,Z, t, maxTop, block='wool', data='0', toSet=False):
    vy = getV0BySt(self.g, self.f, Y-y, t)
    if getTopY(self.g, self.f, vy) <= maxTop - y:
      return [(0, self.getCmdBy2PWithT(x,y,z, X,Y,Z, t, True, block, data, toSet))]
    else:
      vx = getV0BySt(0, self.f, X-x, t)
      vz = getV0BySt(0, self.f, Z-z, t)

      _motion, _t = self.getMotionTBy2PWithTop(x,y,z, X,Y,Z, maxTop)
      _vx,_vy,_vz = _motion
      _t = getTopT(self.g, self.f, _vy)
      _T = int(_t)
      _top = getStByV0(self.g, self.f, _vy, _T)
      ts = [0, _T, t-_T, t]
      xs = [x+getStByV0(0, self.f, vx, value) for value in ts]
      zs = [z+getStByV0(0, self.f, vz, value) for value in ts]
      ys = [y, y+_top, y+_top, Y]
      res= []
      for i in range(3):
        p0=[xs[i],ys[i],zs[i]]
        p1=[xs[i+1],ys[i+1],zs[i+1]]
        ft=ts[i+1]-ts[i]
        noGravity = True if i == 1 else False
        cmd = self.getCmdBy2PWithT(*p0, *p1, ft, not noGravity, block, data, toSet)
        res.append((ts[i], cmd))
      # print(res)
      return res



if __name__ == '__main__':
  FB = FallingBlock()

  x,y,z = 0,4,0
  X,Y,Z = 0,4,16
  top  = 16
  motion, t = FB.getMotionTBy2PWithTop(x+0.5,y,z+0.5, X+0.5,Y,Z+0.5, top)
  for t in range(0,int(t)+1):
    print(FB.getPosBy1PWithV0(x+0.5,y,z+0.5, *motion, t))