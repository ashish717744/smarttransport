#!/usr/bin/env python
# coding: utf-8

# In[2]:


import math as Math
import time


# In[ ]:


import math as Math

def insideGeofence(lat1,lon1,lat2,lon2):
  R = 6371
  dLat = deg2rad(lat2-lat1)
  dLon = deg2rad(lon2-lon1)
  a = Math.sin(dLat/2) * Math.sin(dLat/2) + Math.cos(deg2rad(lat1))     * Math.cos(deg2rad(lat2)) * Math.sin(dLon/2) * Math.sin(dLon/2)
  c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))
  d = R * c
  return True if d > 1 else False

def deg2rad(deg):
  return deg * (Math.pi/180)

