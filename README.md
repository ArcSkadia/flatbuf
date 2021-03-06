# flatbuf
Extended flatbuffers.Builder API making the builder a bit more easy to use.

* single create() method builds both structs and tables
* no need to call Start()/End() for every table/struct being built
* no need for explicitely call Finish() for root types
* client code is not required to order fields explicitly: non-inline build of a struct is fine; nested builds are fine too.
* accept python string as a value for a flatbuffer string field, and python list for a vector field
* values for a vector field is supplied in a natural direct order, not reversed for prepend
* more readable user code as it is no longer required to call into a quite verbose api generated by the fb compiler ( i.e. no calls like Namespace.Type.Type.FooFieldNameCreate(builder, ...). If required, the original builder api methods can be invoked as usual.

## Example 

( using flatbuffers tutorial https://google.github.io/flatbuffers/flatbuffers_guide_tutorial.html )

```python

import flatbuf as flatbuffers 
import MyGame.Sample.Color 
import MyGame.Sample.Equipment 
import MyGame.Sample.Monster 
import MyGame.Sample.Vec3 
import MyGame.Sample.Weapon

bldr = flatbuffers.Builder() 
with bldr.create(MyGame.Sample.Monster) as orc: 
    orc.add('Name', 'Orc')
    sword = bldr.create(MyGame.Sample.Weapon,
                        {'Name': 'Sword', 'Damage': 3})
    axe = bldr.create(MyGame.Sample.Weapon,
                      {'Name': 'Axe', 'Damage': 5})
    orc.add('Weapons', [sword, axe])

    orc.add('EquippedType', MyGame.Sample.Equipment.Equipment.Weapon)
    orc.add('Equipped', axe)

    pos = bldr.create(MyGame.Sample.Vec3, [1.0, 2.0, 3.0])
    orc.add('Pos', pos)
    orc.add('Hp', 300)
    orc.add('Color', MyGame.Sample.Color.Color.Red)

    MyGame.Sample.Monster.MonsterStartInventoryVector(bldr, 10)
    for i in reversed(range(0, 10)):
        bldr.PrependByte(i)
    inv = bldr.EndVector(10)

    orc.add('Inventory', inv)
buf = orc.output()
```

For comparison, same with the flatbuffers builder API: 

```python 
builder = flatbuffers.Builder(0)

weapon_one = builder.CreateString('Sword')
weapon_two = builder.CreateString('Axe')

MyGame.Sample.Weapon.WeaponStart(builder)
MyGame.Sample.Weapon.WeaponAddName(builder, weapon_one)
MyGame.Sample.Weapon.WeaponAddDamage(builder, 3)
sword = MyGame.Sample.Weapon.WeaponEnd(builder)

MyGame.Sample.Weapon.WeaponStart(builder)
MyGame.Sample.Weapon.WeaponAddName(builder, weapon_two)
MyGame.Sample.Weapon.WeaponAddDamage(builder, 5)
axe = MyGame.Sample.Weapon.WeaponEnd(builder)

name = builder.CreateString('Orc')

MyGame.Sample.Monster.MonsterStartInventoryVector(builder, 10)
for i in reversed(range(0, 10)):
    builder.PrependByte(i)
inv = builder.EndVector(10)

MyGame.Sample.Monster.MonsterStartWeaponsVector(builder, 2)

builder.PrependUOffsetTRelative(axe)
builder.PrependUOffsetTRelative(sword)
weapons = builder.EndVector(2)
pos = MyGame.Sample.Vec3.CreateVec3(builder, 1.0, 2.0, 3.0)

MyGame.Sample.Monster.MonsterStart(builder)
MyGame.Sample.Monster.MonsterAddPos(builder, pos)
MyGame.Sample.Monster.MonsterAddHp(builder, 300)
MyGame.Sample.Monster.MonsterAddName(builder, name)
MyGame.Sample.Monster.MonsterAddInventory(builder, inv)
MyGame.Sample.Monster.MonsterAddColor(builder,
                                      MyGame.Sample.Color.Color().Red)
MyGame.Sample.Monster.MonsterAddWeapons(builder, weapons)
MyGame.Sample.Monster.MonsterAddEquippedType(builder, MyGame.Sample.Equipment.Equipment().Weapon)
MyGame.Sample.Monster.MonsterAddEquipped(builder, axe)
orc = MyGame.Sample.Monster.MonsterEnd(builder)

builder.Finish(orc)
buf = builder.Output()
```

