import bpy, os, pytest
from pytest import approx
from mpfb.services.objectservice import ObjectService
from mpfb.services.nodeservice import NodeService
from mpfb.entities.nodemodel.v2 import *

def test_abstractnodewrapper_is_available():
    assert AbstractNodeWrapper

def test_is_valid_assignment():    
    obj = AbstractNodeWrapper({"class": "test"})
    assert obj._check_is_valid_assignment("a", "str")
    assert not obj._check_is_valid_assignment(1, "str")
    assert not obj._check_is_valid_assignment(None, "str")
    assert obj._check_is_valid_assignment([1], "Color")
    assert obj._check_is_valid_assignment([1], "Vector")
    assert obj._check_is_valid_assignment(1, "NodeSocketFloat")
    assert obj._check_is_valid_assignment(0.1, "NodeSocketFloatFactor")
    assert not obj._check_is_valid_assignment("a", "NodeSocketFloatFactor")

def test_can_create_normal_shader_with_defaults():
    node_tree_name = ObjectService.random_name()
    node_tree = NodeService.create_node_tree(node_tree_name)
    node = snBsdfPrincipled.create_instance(node_tree)
    assert node
    assert node.__class__.__name__ == "ShaderNodeBsdfPrincipled"
    node_tree.nodes.remove(node)
    NodeService.destroy_node_tree(node_tree)

def test_can_set_name_and_label():
    node_tree_name = ObjectService.random_name()
    node_tree = NodeService.create_node_tree(node_tree_name)
    node = snBsdfPrincipled.create_instance(node_tree, name="yadayada")
    assert node
    assert node.name == "yadayada"
    assert node.label == "yadayada"
    node_tree.nodes.remove(node)
    node = snBsdfPrincipled.create_instance(node_tree, name="yadayada", label="uggabugga")
    assert node
    assert node.name == "yadayada"
    assert node.label == "uggabugga"
    node_tree.nodes.remove(node)
    NodeService.destroy_node_tree(node_tree)

def test_can_create_normal_shader_with_no_inputs():
    node_tree_name = ObjectService.random_name()
    node_tree = NodeService.create_node_tree(node_tree_name)
    node = snAttribute.create_instance(node_tree)
    assert node
    assert node.__class__.__name__ == "ShaderNodeAttribute"
    node_tree.nodes.remove(node)
    NodeService.destroy_node_tree(node_tree)

def test_will_not_accept_illegal_attribute_name():
    node_tree_name = ObjectService.random_name()
    node_tree = NodeService.create_node_tree(node_tree_name)
    node = None
    with pytest.raises(ValueError):
        node = snBsdfPrincipled.create_instance(node_tree, attribute_values={"yadayada": [-100.0, 200.0]})
    if node:
        node_tree.nodes.remove(node)
    NodeService.destroy_node_tree(node_tree)

def test_will_not_accept_illegal_attribute_value():
    node_tree_name = ObjectService.random_name()
    node_tree = NodeService.create_node_tree(node_tree_name)
    node = None
    with pytest.raises(ValueError):
        node = snBsdfPrincipled.create_instance(node_tree, attribute_values={"location": "uggabugga"})
    if node:
        node_tree.nodes.remove(node)
    NodeService.destroy_node_tree(node_tree)

def test_can_set_array_attribute():
    node_tree_name = ObjectService.random_name()
    node_tree = NodeService.create_node_tree(node_tree_name)
    node = snBsdfPrincipled.create_instance(node_tree, attribute_values={"location": [-100.0, 100.0]})
    assert node
    assert node.location
    assert node.location[1] == approx(100.0)
    node_tree.nodes.remove(node)
    NodeService.destroy_node_tree(node_tree)

def test_can_set_enum_attribute():
    node_tree_name = ObjectService.random_name()
    node_tree = NodeService.create_node_tree(node_tree_name)
    node = snMath.create_instance(node_tree, attribute_values={"operation": "MULTIPLY"})
    assert node
    assert node.operation
    assert node.operation == "MULTIPLY"
    node_tree.nodes.remove(node)
    NodeService.destroy_node_tree(node_tree)

def test_can_set_color_attribute():
    node_tree_name = ObjectService.random_name()
    node_tree = NodeService.create_node_tree(node_tree_name)
    node = snMath.create_instance(node_tree, attribute_values={"color": [0.5, 0.5, 0.0]})
    assert node
    assert node.color
    assert node.color[1] == approx(0.5)
    node_tree.nodes.remove(node)
    NodeService.destroy_node_tree(node_tree)

def test_will_not_accept_illegal_input_socket_name():
    node_tree_name = ObjectService.random_name()
    node_tree = NodeService.create_node_tree(node_tree_name)
    node = None
    with pytest.raises(ValueError):
        node = snBsdfPrincipled.create_instance(node_tree, input_socket_values={"yadayada": [-100.0, 200.0]})
    if node:
        node_tree.nodes.remove(node)
    NodeService.destroy_node_tree(node_tree)

def test_will_not_accept_illegal_input_socket_value():
    node_tree_name = ObjectService.random_name()
    node_tree = NodeService.create_node_tree(node_tree_name)
    node = None
    with pytest.raises(ValueError):
        node = snBsdfPrincipled.create_instance(node_tree, input_socket_values={"Base Color": "uggabugga"})
    if node:
        node_tree.nodes.remove(node)
    NodeService.destroy_node_tree(node_tree)

def test_can_set_color_input_socket():
    node_tree_name = ObjectService.random_name()
    node_tree = NodeService.create_node_tree(node_tree_name)
    node = snBsdfPrincipled.create_instance(node_tree, input_socket_values={"Base Color": [0.5, 0.5, 0.0, 0.0]})
    assert node
    input = node.inputs["Base Color"]
    assert len(input.default_value) == 4
    assert input.default_value[1] == approx(0.5) 
    node_tree.nodes.remove(node)
    NodeService.destroy_node_tree(node_tree)

def test_can_set_float_factor_input_socket():
    node_tree_name = ObjectService.random_name()
    node_tree = NodeService.create_node_tree(node_tree_name)
    node = snBsdfPrincipled.create_instance(node_tree, input_socket_values={"Alpha": 0.5})
    assert node
    input = node.inputs["Alpha"]    
    assert input.default_value == approx(0.5) 
    node_tree.nodes.remove(node)
    NodeService.destroy_node_tree(node_tree)

def test_can_set_vector_input_socket():
    node_tree_name = ObjectService.random_name()
    node_tree = NodeService.create_node_tree(node_tree_name)
    node = snBsdfPrincipled.create_instance(node_tree, input_socket_values={"Subsurface Radius": [0.3, 0.3, 0.3]})
    assert node
    input = node.inputs["Subsurface Radius"]    
    assert input.default_value[1] == approx(0.3) 
    node_tree.nodes.remove(node)
    NodeService.destroy_node_tree(node_tree)

def test_can_set_float_input_socket():
    node_tree_name = ObjectService.random_name()
    node_tree = NodeService.create_node_tree(node_tree_name)
    node = snMath.create_instance(node_tree, input_socket_values={"Value": 0.1})
    assert node
    input = node.inputs["Value"]    
    assert input.default_value == approx(0.1) 
    node_tree.nodes.remove(node)
    NodeService.destroy_node_tree(node_tree)

def test_can_set_input_socket_by_identifier():
    node_tree_name = ObjectService.random_name()
    node_tree = NodeService.create_node_tree(node_tree_name)
    node = snMath.create_instance(node_tree, input_socket_values={"Value_001": 0.1})
    assert node
    input = None
    for socket in node.inputs:
        if socket.identifier == "Value_001":
            input = socket
    assert input
    assert input.default_value == approx(0.1) 
    node_tree.nodes.remove(node)
    NodeService.destroy_node_tree(node_tree)

def test_can_set_float_output_socket():
    node_tree_name = ObjectService.random_name()
    node_tree = NodeService.create_node_tree(node_tree_name)
    node = snValue.create_instance(node_tree, output_socket_values={"Value": 0.1})
    assert node
    output = node.outputs["Value"]    
    assert output.default_value == approx(0.1) 
    node_tree.nodes.remove(node)
    NodeService.destroy_node_tree(node_tree)

def test_can_set_color_output_socket():
    node_tree_name = ObjectService.random_name()
    node_tree = NodeService.create_node_tree(node_tree_name)
    node = snRGB.create_instance(node_tree, output_socket_values={"Color": [0.1, 0.1, 0.1, 0.1]})
    assert node
    output = node.outputs["Color"]    
    assert output.default_value[1] == approx(0.1) 
    node_tree.nodes.remove(node)
    NodeService.destroy_node_tree(node_tree)
