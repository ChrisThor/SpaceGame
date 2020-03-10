# SpaceGame

This game requires the pygame package. Use `pip install pygame` to install it.

### Controls

- Accelerate forward: Arrow up
- Accelerate backward: Arrow down
- Turn left: Arrow left
- Turn right: Arrow right
- Break: g
- Zoom +: F2
- Zoom -: F1
- Save Space Objects: F5
- Load Space Objects: F9
- Increase Simulation Speed: e
- Decrease Simulation Speed: q
- Increase Thrust Strength: w
- Decrease Thrust Strength: s
- Pause Simulation: p
- Show speed and acceleration vectors: v
- Place Planet: left mousebutton

When placing planets, there are additional controls to customize their properties.
- Hold c while pressing the left mouse button to let that object ignore gravitational acceleration.
- Press x to switch between radius and mass mode
- Use the mouse wheel to in- or decrease the space object's mass or radius.
- Press the right mouse button to set the speed vector. It will be indicated by a blueish line.
- Press the left mouse button a second time to create the planet.

## Worlds

When accessing a world, controls are completely different. 
- Movement: a, s
- Jump: Space
- Switch tool mode: x
- Manipulate foreground: left mousebutton
- Manipulate background: right mousebutton
- Place Object: left mousebutton
- Command mode: Enter

### Commands
*Commands* are currently only accessible on worlds.

`give`:
This command uses two parameters. The first parameter can be `o` or `object` for requesting a placable object
and `b` or `block` is used for blocks. The second parameter is the filename of the specific object or block.

**Examples:** 

```
give o wooden_table
give b dirt
```

`tp`:
This command will teleport the player to a specified position. This command requires two parameters of which the
first parameter is the x value of the position and the second parameter is the y value. If you'd like to give a
relative position, use `~` as a prefix. If you only use `~`, it will count as a `0`. It is possible to use relative coordinates for one axis while using absolute
coordinates for the other.

Instead of coordinates, tp also accepts the parameter `spawn`. This will teleport the player to the spawn point of
a world.

**NOTE:** The coordinate system is structured in a way that has the effect that positive y values point to the
bottom of the screen.

**Examples:**
```
tp -40 40
tp ~ ~-32
tp ~1 0
tp spawn
```

`setspawn`:
This command sets the spawnpoint and uses the same syntax like the `tp` command, which means that the spawn can be
defined with absolute coordinates or relative coordinates to the player. However, it does not support setting the
spawn with the spawn.

It is also possible to use the  command without any parameters. This would be equivalent to `setspawn ~ ~`.

**Examples:**
```
setspawn
setspawn 0 0
```
