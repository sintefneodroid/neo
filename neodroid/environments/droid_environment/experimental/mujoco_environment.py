#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 8/17/22
           """

__all__ = []

from pathlib import Path

if True:
    import mujoco

    s = Path("/home/heider/SynologyDrive/personal/ModelsPersonalSonylogy/gizmo.stl")
    if False:
        XML = r"""
    <mujoco>
      <asset>
        <mesh file="gizmo.stl"/>
      </asset>
      <worldbody>
        <body>
          <freejoint/>
          <geom type="mesh" name="gizmo" mesh="gizmo"/>
        </body>
      </worldbody>
    </mujoco>
    """
    else:
        XML = r"""<mujoco>
    <option iterations="10" tolerance="0" gravity="-1 0 -10" jacobian="dense">
      <flag fwdinv="enable" energy="enable"/>
    </option>
  
    <asset>
      <mesh name="icosahedron" scale=".05 .05 .05"
            vertex="0         1       1.618
                    0        -1       1.618
                    0         1      -1.618
                    0        -1      -1.618
                    1         1.618   0
                   -1         1.618   0
                    1        -1.618   0
                   -1        -1.618   0
                    1.618     0       1
                    1.618     0      -1
                   -1.618     0       1
                   -1.618     0      -1"/>
      <hfield name="hfield" nrow="3" ncol="3" size=".2 .2 .1 .03"/>
    </asset>
  
    <default>
      <site rgba=".5 .5 .5 .5"/>
      <joint armature="1" damping="10"/>
      <general ctrllimited="true" ctrlrange="-1 1"/>
      <default class="hip0">
        <joint springref="30" stiffness="60"/>
      </default>
      <default class="hip1">
        <joint limited="true" range="-60 60" stiffness="10"/>
      </default>
      <default class="wheel">
        <joint damping=".1" armature=".1"/>
      </default>
    </default>
  
    <worldbody>
      <light pos="0 0 3"/>
      <geom type="plane" size="4 4 .1"/>
      <geom type="hfield" hfield="hfield" pos="-.4 .6 .05" rgba="0 0 1 1"/>
      <body name="head" pos="0 0 .7">
        <geom type="ellipsoid" size=".2 .2 .4" rgba="1 1 0 1" density="100"/>
        <site name="head" pos="0 0 .4" size=".1 .1 .05" type="box"/>
        <site name="anchor0" pos="0 .2 0"/>
        <site name="rf" pos="0 0 -0.41" zaxis="0 0 -1"/>
        <freejoint/>
        <body euler="0 0 0" pos=".2 0 -.2">
          <joint name="hipz_0" class="hip1" axis="0 0 1"/>
          <joint name="hipy_0" class="hip0" axis="0 1 0"/>
          <geom type="capsule" size=".05" rgba="1 0 0 1" fromto="0 0 0 .3 0 0"/>
          <body pos=".3 0 0">
            <site name="knee"/>
            <geom type="capsule" size=".05" rgba="1 0 0 1" fromto="0 0 0 .1 0 -.3"/>
            <body pos=".1 0 -.3">
              <joint name="wheel_0" type="ball" class="wheel"/>
              <site name="wheel_0" type="box" size=".1 .1 .1"/>
              <geom size=".1 .2 .1"  rgba="0 1 0 1" type="ellipsoid"/>
            </body>
          </body>
        </body>
        <body euler="0 0 120" pos="-.15 .2 -.2">
          <joint name="hipz_1" class="hip1" axis="0 0 1"/>
          <joint name="hipy_1" class="hip0" axis="0 1 0"/>
          <geom type="box" size=".05" rgba="1 0 0 1" fromto="0 0 0 .3 0 0"/>
          <geom type="box" size=".05" rgba="1 0 0 1" fromto=".3 0 0 .4 0 -.3"/>
          <body pos=".45 0 -.3">
            <joint name="wheel_1" axis="1 0 0" class="wheel"/>
            <geom size=".1"  rgba="0 1 0 1" type="cylinder" fromto="0 0 0 .03 0 0"/>
            <site name="wheel_1" type="box" size=".02 .11 .11" pos=".015 0 0"/>
          </body>
        </body>
        <body euler="0 0 240" pos="-.15 -.2 -.2">
          <joint name="hipz_2" class="hip1" axis="0 0 1"/>
          <joint name="hipy_2" class="hip0" axis="0 1 0"/>
          <geom type="capsule" size=".05" rgba="1 0 0 1" fromto="0 0 0 .3 0 0"/>
          <geom type="capsule" size=".05" rgba="1 0 0 1" fromto=".3 0 0 .4 0 -.3"/>
          <body pos=".45 0 -.3">
            <joint name="wheel_2" axis="1 0 0" class="wheel"/>
            <geom size=".1"  rgba="0 1 0 1" type="cylinder" fromto="0 0 0 .03 0 0"/>
            <site name="wheel_2" size=".13"  rgba="0 0 0 0.1" type="cylinder" fromto="-.01 0 0 .04 0 0"/>
          </body>
        </body>
      </body>
      <body pos="-.33 0 1">
        <joint name="slider" type="slide" axis="0 0 1" limited="true" range="-.2 .5"/>
        <joint type="hinge" axis="0 1 0"/>
        <geom type="mesh" mesh="icosahedron" size=".1" rgba="0 0 1 1"/>
      </body>
      <body name="cylinder" pos="-.5 .3 .7">
        <freejoint/>
        <geom name="wrapping" type="cylinder" size=".04" fromto="-.1 -.2 0 .1 .4 0"/>
        <site name="cylinder"/>
      </body>
      <site name="sidesite" pos="-.5 .4 1"/>
      <body pos="-.3 .6 .8">
        <freejoint/>
        <geom type="box" size=".05 .05 .05" rgba="0 0 1 1"/>
        <site name="anchor1" pos=".05 .05 .05"/>
      </body>
      <body pos="-.6 .4 .8">
        <freejoint/>
        <geom type="box" size=".05 .05 .05" rgba="0 0 1 1"/>
        <site name="anchor2" pos=".05 .05 .05"/>
      </body>
    </worldbody>
  
    <equality>
      <weld body1="cylinder" body2="world"/>
    </equality>
  
    <tendon>
      <spatial name="spatial" limited="true" range="0 .7" rgba="1 0 1 1">
        <site site="anchor0"/>
        <site site="anchor1"/>
        <geom geom="wrapping" sidesite="sidesite"/>
        <site site="anchor2"/>
      </spatial>
      <fixed name="fixed">
        <joint joint="hipy_0" coef="1"/>
        <joint joint="hipy_1" coef="1"/>
      </fixed>
    </tendon>
  
    <actuator>
      <motor tendon="fixed" gear="100"/>
      <motor tendon="spatial" gear="10"/>
      <motor joint="hipy_2" gear="100"/>
      <position joint="hipz_1" kp="100"/>
      <position joint="hipz_2" kp="100"/>
      <velocity joint="wheel_2" kv="1"/>
      <intvelocity joint="hipz_0" kp="100" actrange="-1 1"/>
      <general site="wheel_0" gear="0 0 0 0 10 0" dyntype="filter" dynprm="1"/>
      <general joint="wheel_1" biastype="affine" dyntype="integrator" dynprm="1" biasprm="0 -1"/>
    </actuator>
  
    <sensor>
      <framepos objtype="site" objname="wheel_0" reftype="site" refname="wheel_2"/>
      <rangefinder site="rf"/>
      <gyro site="wheel_2"/>
      <touch site="wheel_1"/>
      <force site="knee"/>
      <torque site="knee"/>
      <force site="cylinder"/>
      <torque site="cylinder"/>
      <jointlimitfrc joint="slider"/>
      <accelerometer site="head"/>
      <subtreeangmom body="head"/>
    </sensor>
  </mujoco>"""

    ASSETS = dict()
    with open(str(s), "rb") as f:
        ASSETS["gizmo.stl"] = f.read()
    # from mujoco import MjModel, MjSim, MjViewer
    # from mujoco.rollout import rollout

    model = mujoco.MjModel.from_xml_string(XML, ASSETS)  # maybe? pip install mujoco-py
    data = mujoco.MjData(model)
    while data.time < 1:
        mujoco.mj_step(model, data)
        print(data.geom_xpos)

    # state, sensordata = rollout.rollout(model, data, initial_state, ctrl)

if False:
    import gym

    env = gym.make("Humanoid-v4")
    print("\nIt is OKAY!" if env.reset() is not None else "\nSome problem here...")


if False:
    import mujoco_py
    import os

    mj_path = mujoco_py.utils.discover_mujoco()
    xml_path = os.path.join(mj_path, "model", "humanoid.xml")
    model = mujoco_py.load_model_from_path(xml_path)
    sim = mujoco_py.MjSim(model)

    print(sim.data.qpos)
    # [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]

    sim.step()
    print(sim.data.qpos)

if False:
    from dm_control import suite

    env = suite.load("cartpole", "swingup")
    pixels = env.physics.render()
