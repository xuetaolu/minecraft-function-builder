# bilibili
# @Bio-Hazard, @xue_tao_lu, @Medit_4

from math import log
from math import e

# 各种类型的竖直加速度以及助力，单位为 block/tick^2
DataTable = {
  1:{'g':-0.08, 'f':0.02},
  2:{'g':-0.04, 'f':0.02},
  3:{'g':-0.04, 'f':0.05},
  4:{'g':-0.03, 'f':0.01},
  5:{'g':-0.05, 'f':0.01},
}

# 各种实体对应的类型id
EntityType={
  'player':1,
  'living':1,
  'item':2,
  'fallingBlock':2,
  'tnt':2,
  'boat':3,
  'minecart':3,
  'egg':4,
  'snowball':4,
  'potion':4,
  'enderPearl':4,
  'arrow':5
}  

def ln(x):
  return log(x, e)


def getGFById(_id):
  data = DataTable[_id]
  return data['g'], data['f']

def getGFByType(_type):
  return getGFById(EntityType[_type])


# 通用公式
def getVtByV0(g, f, v0, t):
  '''通过 v0 求 vt，水平方向 g=0'''
  return (v0+g-g/f)*(1-f)**(t-1) + g/f

def getStByV0(g, f, v0, t):
  '''通过 v0 求 St，水平方向 g=0'''
  return (v0+g-g/f)*(1-(1-f)**t)/f + g/f*t

def getV0BySt(g, f, St, t):
  '''通过 St 方向求 v0，水平方向 g=0'''
  return (f*St-g*t)/(1-(1-f)**t) + g/f - g

def getTopT(g, f, vy):
  '''最高时刻 t'''
  return ( ln(-g) - ln(-ln(1-f)) - ln(vy+g-g/f) ) / ln(1-f)

def getTopY(g, f, vy):
  '''最高高度 t'''
  if vy <= 0:
    print(f'[Warning]: In api_motion getTopY, vy({vy}) <= 0')
    return getVtByV0(g, f, vy, 0)
  else:
    t = getTopT(g, f, vy)
    return getStByV0(g, f, vy, t)

def getTopTY(g, f, vy):
  t = getTopT(g, f, vy)
  return t, getStByV0(g, f, vy, t)

def getSyBySx(g, f, vx, vy, Sx):
  '''已知Vx0, Vy0, 通过 Sx 求 Sy'''
  return (vy+g-g/f)*x/vx + ( g/f * (1-ln(f*Sx)/vx) / ln(1-f) )


def getTByStWithTop(g,f, St, Top, limit=0.5):
  '''给定St，求固定高度代码方程 Top = maxY - S0'''
  t0, t1 = 0, 600
  while (t1-t0) > limit:
    t = 0.5*(t1+t0)
    v0= getV0BySt(g,f, St, t)
    _t, _top = getTopTY(g,f, v0)
    if _top < Top:
      t0 = t
    else:
      t1 = t
  return 0.5*(t1+t0)

def getDownTBySt(g, f, St, limit=0.5):
  '''求自由落体 St 需要的时间, St > 0'''
  v0     = 0.0
  t0, t1 = 0.0, 600.0
  while (t1-t0) > limit:
    t = 0.5*(t0+t1)
    S = -getStByV0(g,f, v0, t)
    if S > St:
      t1 = t
    else:
      t0 = t
  return 0.5*(t1+t0)

def getUpTBySt(g, f, St, limit=0.5):
  '''求上升 St 刚好 vy = 0, 需要的时间, St > 0'''
  v0     = 0.0
  t0, t1 = -600.0, 0.0
  while (t1-t0) > limit:
    t = 0.5*(t0+t1)
    S = -getStByV0(g,f, v0, t)
    if S > St:
      t0 = t
    else:
      t1 = t
  return 0.5*(t1+t0)


if __name__ == '__main__':
  # print(getGFById(1))
  # print(getGFByType('fallingBlock'))


  g,f = getGFByType('fallingBlock')
  print(f'g:{g}, f:{f}')

  # for tick in range(50):
  #   print(tick, getStByV0(g,f,1.0,tick))

  # print(getTopTY(g,f, 1.0))

  # print(getTopTY(g,f, -1.0))
  # 
  # 
  
  height = 20
  t0 = getUpTBySt(g,f, height)
  t1 = getDownTBySt(g,f, height)
  print(f'h:{height}, t0:{t0}, t1:{t1}')



  pass


