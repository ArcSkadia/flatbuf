import unittest
import sys

import flatbuf as flatbuffers

import fbs_test.Composite
import fbs_test.Identity
import fbs_test.Color
import fbs_test.Location


class TestFlatBuf(unittest.TestCase):

    def test_identify(self):

        from flatbuf._builder import identify

        r = identify(fbs_test.Composite.Composite)
        self.assertEqual(r[0], 'Composite')
        self.assertEqual(r[1], fbs_test.Composite)

        r = identify(fbs_test.Composite)
        self.assertEqual(r[0], 'Composite')
        self.assertEqual(r[1], fbs_test.Composite)

        r = identify(fbs_test.Composite.Composite.Bytes)
        self.assertEqual(r[0], 'Bytes')
        self.assertEqual(r[1], fbs_test.Composite)

        from fbs_test.Location import Location as Bar
        r = identify(Bar)
        self.assertEqual(r[0], 'Location')
        self.assertEqual(r[1], fbs_test.Location)

    def test_is_struct(self):
        from flatbuf._builder import is_struct, identify
        self.assertFalse(is_struct(identify(fbs_test.Composite)))
        self.assertTrue(is_struct(identify(fbs_test.Color)))
        self.assertTrue(is_struct(identify(fbs_test.Location)))
        self.assertFalse(is_struct(identify(fbs_test.Identity)))

        self.assertFalse(is_struct(identify(fbs_test.Composite.Composite)))
        self.assertTrue(is_struct(identify(fbs_test.Color.Color)))
        self.assertTrue(is_struct(identify(fbs_test.Location.Location)))
        self.assertFalse(is_struct(identify(fbs_test.Identity.Identity)))

    def test_create_target(self):

        bldr = flatbuffers.Builder()
        ref = [bldr.create(fbs_test.Identity.Identity, {'Id': 1, 'Key': '2'}),
               bldr.create(fbs_test.Identity.Identity, {'Id': 3, 'Key': '4'})]

        enc = bldr.create(fbs_test.Composite.Composite,
                          {'Loc': bldr.create(fbs_test.Location, [1, 2]),
                           'RefData': ref})

        def _check(msg):
            r = fbs_test.Composite.Composite.GetRootAsComposite(msg, 0)
            self.assertEqual(r.Loc().X(), 1)
            self.assertEqual(r.Loc().Y(), 2)

            self.assertEqual(r.RefDataLength(), 2)
            self.assertEqual(r.RefData(0).Id(), 1)
            self.assertEqual(r.RefData(1).Id(), 3)
            self.assertEqual(r.RefData(0).Key(), '2')
            self.assertEqual(r.RefData(1).Key(), '4')

        _check(bldr.finish(enc).Output())

        #--------------------------------------------------

        from fbs_test.Identity import Identity as IdentityCls
        from fbs_test.Composite import Composite as CompositeCls

        bldr = flatbuffers.Builder()
        ref = [bldr.create(IdentityCls, {'Id': 1, 'Key': '2'}),
               bldr.create(IdentityCls, {'Id': 3, 'Key': '4'})]
        enc = bldr.create(CompositeCls,
                          {'Loc': bldr.create(fbs_test.Location, [1, 2]),
                           'RefData': ref})
        _check(bldr.finish(enc).Output())

        #--------------------------------------------------

        import fbs_test.Identity as IdentityModule
        import fbs_test.Composite as CompositeModule

        bldr = flatbuffers.Builder()
        ref = [bldr.create(IdentityModule, {'Id': 1, 'Key': '2'}),
               bldr.create(IdentityModule, {'Id': 3, 'Key': '4'})]

        enc = bldr.create(CompositeModule,
                          {'Loc': bldr.create(fbs_test.Location, [1, 2]),
                           'RefData': ref})
        _check(bldr.finish(enc).Output())

    def test_free_order(self):

        def _create_records(builder):
            return [builder.create(fbs_test.Identity, {'Id': 1, 'Key': 'abc'}),
                    builder.create(fbs_test.Identity, {'Id': 9, 'Key': 'unknown'})]
        rgb = [120.0, 250.0, 64.0]
        xy = [42, -42]

        def _check(msg):
            r = fbs_test.Composite.Composite.GetRootAsComposite(msg, 0)

            self.assertEqual(r.Name(), 'utest')

            self.assertEqual(r.Loc().X(),  42)
            self.assertEqual(r.Loc().Y(), -42)

            self.assertAlmostEqual(r.Shade().Red(),   120.0)
            self.assertAlmostEqual(r.Shade().Green(), 250.0)
            self.assertAlmostEqual(r.Shade().Blue(),   64.0)

            self.assertEqual(r.RefDataLength(), 2)
            self.assertEqual(r.RefData(0).Id(), 1)
            self.assertEqual(r.RefData(1).Id(), 9)
            self.assertEqual(r.RefData(0).Key(), 'abc')
            self.assertEqual(r.RefData(1).Key(), 'unknown')

        #---------------------------------------------
        bldr = flatbuffers.Builder()
        records = _create_records(bldr)
        color = bldr.create(fbs_test.Color, rgb)
        location = bldr.create(fbs_test.Location, xy)

        enc = bldr.create(fbs_test.Composite, properties={'Shade': color,
                                                          'Name': 'utest',
                                                          'Loc': location,
                                                          'RefData': records})
        _check(bldr.finish(enc).Output())

        #---------------------------------------------
        bldr = flatbuffers.Builder()
        records = _create_records(bldr)
        enc = bldr.create(fbs_test.Composite,
                          properties=[('Shade', bldr.create(fbs_test.Color, rgb)),
                                      ('Name', 'utest'),
                                      ('Loc', bldr.create(fbs_test.Location, xy)),
                                      ('RefData', records)])
        _check(bldr.finish(enc).Output())

        #---------------------------------------------
        bldr = flatbuffers.Builder()
        records = _create_records(bldr)
        enc = bldr.create(fbs_test.Composite,
                          properties=[('Loc', bldr.create(fbs_test.Location, xy)),
                                      ('Shade', bldr.create(fbs_test.Color, rgb)),
                                      ('Name', 'utest'),
                                      ('RefData', records)])
        _check(bldr.finish(enc).Output())

        #---------------------------------------------
        bldr = flatbuffers.Builder()
        records = _create_records(bldr)
        enc = bldr.create(fbs_test.Composite,
                          properties=[('Name', 'utest'),
                                      ('RefData', records),
                                      ('Loc', bldr.create(fbs_test.Location, xy)),
                                      ('Shade', bldr.create(fbs_test.Color, rgb))])
        _check(bldr.finish(enc).Output())

        #---------------------------------------------


class TestBuildMgr(unittest.TestCase):

    def test_free_order(self):

        #---------------------------------------------

        def _create_records(builder):
            return [builder.create(fbs_test.Identity, {'Id': 1, 'Key': 'abc'}),
                    builder.create(fbs_test.Identity, {'Id': 9, 'Key': 'unknown'})]
        rgb = [120.0, 250.0, 64.0]
        xy = [42, -42]

        def _check(msg):
            r = fbs_test.Composite.Composite.GetRootAsComposite(msg, 0)

            self.assertEqual(r.Name(), 'utest')

            self.assertEqual(r.Loc().X(),  42)
            self.assertEqual(r.Loc().Y(), -42)

            self.assertAlmostEqual(r.Shade().Red(),   120.0)
            self.assertAlmostEqual(r.Shade().Green(), 250.0)
            self.assertAlmostEqual(r.Shade().Blue(),   64.0)

            self.assertEqual(r.RefDataLength(), 2)
            self.assertEqual(r.RefData(0).Id(), 1)
            self.assertEqual(r.RefData(1).Id(), 9)
            self.assertEqual(r.RefData(0).Key(), 'abc')
            self.assertEqual(r.RefData(1).Key(), 'unknown')

        #---------------------------------------------
        bldr = flatbuffers.Builder()
        records = _create_records(bldr)
        color = bldr.create(fbs_test.Color, rgb)
        location = bldr.create(fbs_test.Location, xy)

        with bldr.create(fbs_test.Composite) as c:
            c.add('Shade', color)
            c.add('Name', 'utest')
            c.add('Loc', location)
            c.add('RefData', records)
        _check(c.output())

        #---------------------------------------------
        bldr = flatbuffers.Builder()
        with bldr.create(fbs_test.Composite) as c:
            c.add('Shade', bldr.create(fbs_test.Color, rgb))
            c.add('Name', 'utest')
            c.add('Loc', bldr.create(fbs_test.Location, xy))
            c.add('RefData', _create_records(bldr))
        _check(c.output())

        #----------------------------------------------
        bldr = flatbuffers.Builder()
        with bldr.create(fbs_test.Composite) as c:
            c.add('Loc', bldr.create(fbs_test.Location, xy))
            c.add('Shade', bldr.create(fbs_test.Color, rgb))
            c.add('Name', 'utest')
            c.add('RefData', _create_records(bldr))
        _check(c.output())

        #----------------------------------------------
        bldr = flatbuffers.Builder()
        with bldr.create(fbs_test.Composite) as c:
            c.add('RefData', _create_records(bldr))
            c.add('Name', 'utest')
            c.add('Loc', bldr.create(fbs_test.Location, xy))
            c.add('Shade', bldr.create(fbs_test.Color, rgb))
        _check(c.output())

    def test_build_inline(self):
        bldr = flatbuffers.Builder()

        location = flatbuffers.build_inline(fbs_test.Location.CreateLocation, values=[5, 6])
        color = flatbuffers.build_inline(fbs_test.Color.CreateColor, values=[0.1, 0.2, 0.3])

        with bldr.create(fbs_test.Composite) as c:
            c.add('Loc', location)
            c.add('Shade', color)

        msg = c.output()
        r = fbs_test.Composite.Composite.GetRootAsComposite(msg, 0)

        self.assertAlmostEqual(r.Shade().Red(), 0.1)
        self.assertAlmostEqual(r.Shade().Green(), 0.2)
        self.assertAlmostEqual(r.Shade().Blue(), 0.3)

        self.assertEqual(r.Loc().X(), 5)
        self.assertEqual(r.Loc().Y(), 6)

    def test_multiple_finalize(self):

        with flatbuffers.Builder().create(fbs_test.Composite) as c:
            c.add('Name', 'abc')

        r0 = c.output()  # calls c._finalize()
        r1 = c.output()
        r2 = c.output()

        self.assertEqual(fbs_test.Composite.Composite.GetRootAsComposite(r1, 0).Name(), 'abc')
        self.assertEqual(fbs_test.Composite.Composite.GetRootAsComposite(r2, 0).Name(), 'abc')
        self.assertEqual(fbs_test.Composite.Composite.GetRootAsComposite(r0, 0).Name(), 'abc')

    def test_scalar_vectors(self):
        bldr = flatbuffers.Builder()

        # todo find a better way to create scalar vectors
        data = [1, 2, 3]
        fbs_test.Composite.CompositeStartBytesVector(bldr, len(data))
        for i in reversed(data):
            bldr.PrependByte(i)
        b = bldr.EndVector(len(data))

        with bldr.create(fbs_test.Composite) as c:
            c.add('Bytes', b)

        r = fbs_test.Composite.Composite.GetRootAsComposite(c.output(), 0)

        self.assertEqual(r.BytesLength(), 3)
        self.assertEqual(r.Bytes(0), 1)
        self.assertEqual(r.Bytes(1), 2)
        self.assertEqual(r.Bytes(2), 3)

    def test_field_name_error(self):
        from flatbuf._builder import locate

        self.assertTrue(locate(fbs_test.Composite, 'CompositeAddShade') is not None)

        with self.assertRaises(AttributeError):
            locate(fbs_test.Composite, 'boo')

        with self.assertRaises(AttributeError) as err:
            locate(fbs_test.Composite, 'CompositeAddshade')
        self.assertTrue('CompositeAddshade' in str(err.exception))
        self.assertTrue('field name Shade' in str(err.exception))

        with self.assertRaises(AttributeError) as err:
            locate(fbs_test.Composite, 'CompositeStartrefdataVector')
        self.assertTrue('CompositeStartRefDataVector' in str(err.exception))
        self.assertTrue('field name RefData' in str(err.exception))

        with self.assertRaises(AttributeError) as err:
            locate(fbs_test.Composite, 'CompositeStartref_dataVector')
        self.assertTrue('CompositeStartRefDataVector' in str(err.exception))
        self.assertTrue('field name RefData' in str(err.exception))

        with self.assertRaises(AttributeError) as err:
            with flatbuffers.Builder().create(fbs_test.Composite) as c:
                c.add('ref_data', [1, 2])
        self.assertTrue('CompositeAddRefData' in str(err.exception))
        self.assertTrue('field name RefData' in str(err.exception))


if __name__ == '__main__':
    unittest.main()
