from util.math.vector3 import Vector3

Test_Verts = [
        Vector3([0, 0, 0], data_type=float),
        Vector3([0, 1, 0], data_type=float),
        Vector3([0, 1, 1], data_type=float),
        Vector3([0, 0, 1], data_type=float),
    ]

Test_Tris_Index = [
    Vector3([0, 1, 2]),
    Vector3([1, 2, 3])
]

if __name__ == '__main__':
    from solo_mesh import SoloMesh
    from recast.geom import Geom
    from recast.build_config import BuildConfig
    from recast.context import Context
    context = Context()
    config = BuildConfig()
    geom = Geom(verts=Test_Verts, tris_index=Test_Tris_Index)
    soleMesh = SoloMesh(context, config, geom)
