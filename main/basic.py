from symbol_table import SymbolTable
from strings_with_arrows import *
from context import Context
from errors import RTError
from draw import draw_exp
from parser import Parser
from lexer import Lexer
from tokens import *
import math
import os

# RUNTIME RESULT
class RTResult:
  def __init__(self):
    self.reset()

  def reset(self):
    self.value = None
    self.error = None
    self.func_return_value = None
    self.loop_should_continue = False
    self.loop_should_break = False

  def register(self, res):
    self.error = res.error
    self.func_return_value = res.func_return_value
    self.loop_should_continue = res.loop_should_continue
    self.loop_should_break = res.loop_should_break
    return res.value

  def success(self, value):
    self.reset()
    self.value = value
    return self

  def success_return(self, value):
    self.reset()
    self.func_return_value = value
    return self
  
  def success_continue(self):
    self.reset()
    self.loop_should_continue = True
    return self

  def success_break(self):
    self.reset()
    self.loop_should_break = True
    return self

  def failure(self, error):
    self.reset()
    self.error = error
    return self

  def should_return(self):
    # Note: this will allow you to continue and break outside the current function
    return (
      self.error or
      self.func_return_value or
      self.loop_should_continue or
      self.loop_should_break
    )

# VALUES
class Value:
  def __init__(self):
    self.set_pos()
    self.set_context()

  def set_pos(self, pos_start=None, pos_end=None):
    self.pos_start = pos_start
    self.pos_end = pos_end
    return self

  def set_context(self, context=None):
    self.context = context
    return self

  def added_to(self, other):
    return None, self.illegal_operation(other)

  def subbed_by(self, other):
    return None, self.illegal_operation(other)

  def multed_by(self, other):
    return None, self.illegal_operation(other)

  def dived_by(self, other):
    return None, self.illegal_operation(other)

  def moded_by(self, other):
    return None, self.illegal_operation(other)

  def powed_by(self, other):
    return None, self.illegal_operation(other)

  def get_comparison_eq(self, other):
    return None, self.illegal_operation(other)

  def get_comparison_ne(self, other):
    return None, self.illegal_operation(other)

  def get_comparison_lt(self, other):
    return None, self.illegal_operation(other)

  def get_comparison_gt(self, other):
    return None, self.illegal_operation(other)

  def get_comparison_lte(self, other):
    return None, self.illegal_operation(other)

  def get_comparison_gte(self, other):
    return None, self.illegal_operation(other)

  def anded_by(self, other):
    return None, self.illegal_operation(other)

  def ored_by(self, other):
    return None, self.illegal_operation(other)

  def notted(self, other):
    return None, self.illegal_operation(other)

  def execute(self, args):
    return RTResult().failure(self.illegal_operation())

  def copy(self):
    raise Exception('No copy method defined')

  def is_true(self):
    return False

  def illegal_operation(self, other=None):
    if not other: other = self
    return RTError(
      self.pos_start, other.pos_end,
      'Illegal operation',
      self.context
    )

class Number(Value):
  def __init__(self, value):
    super().__init__()
    self.value = value

  def to_realnum(self):
    num = float(self.value) if (float(self.value) % 1) else int(self.value)
    return num

  def added_to(self, other):
    if isinstance(other, Number):
      return Number(self.value + other.value).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def subbed_by(self, other):
    if isinstance(other, Number):
      return Number(self.value - other.value).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def multed_by(self, other):
    if isinstance(other, Number):
      return Number(self.value * other.value).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def dived_by(self, other):
    if isinstance(other, Number):
      if other.value == 0:
        return None, RTError(
          other.pos_start, other.pos_end,
          'Division by zero',
          self.context
        )

      return Number(self.value / other.value).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def moded_by(self, other):
    if isinstance(other, Number):
      if other.value == 0:
        return None, RTError(
          other.pos_start, other.pos_end,
          'Mod by zero',
          self.context
        )

      return Number(self.value % other.value).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def powed_by(self, other):
    if isinstance(other, Number):
      return Number(self.value ** other.value).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def get_comparison_eq(self, other):
    if isinstance(other, Number):
      return Number(int(self.value == other.value)).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def get_comparison_ne(self, other):
    if isinstance(other, Number):
      return Number(int(self.value != other.value)).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def get_comparison_lt(self, other):
    if isinstance(other, Number):
      return Number(int(self.value < other.value)).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def get_comparison_gt(self, other):
    if isinstance(other, Number):
      return Number(int(self.value > other.value)).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def get_comparison_lte(self, other):
    if isinstance(other, Number):
      return Number(int(self.value <= other.value)).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def get_comparison_gte(self, other):
    if isinstance(other, Number):
      return Number(int(self.value >= other.value)).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def anded_by(self, other):
    if isinstance(other, Number):
      return Number(int(self.value and other.value)).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def ored_by(self, other):
    if isinstance(other, Number):
      return Number(int(self.value or other.value)).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def notted(self):
    return Number(1 if self.value == 0 else 0).set_context(self.context), None

  def copy(self):
    copy = Number(self.value)
    copy.set_pos(self.pos_start, self.pos_end)
    copy.set_context(self.context)
    return copy

  def is_true(self):
    return self.value != 0

  def __str__(self):
    return str(self.value)
  
  def __repr__(self):
    return str(self.value)

Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)
Number.math_PI = Number(math.pi)
Number.math_E = Number(math.e)

class String(Value):
  def __init__(self, value):
    super().__init__()
    self.value = value

  def to_str(self):
    num = str(self.value)
    return num

  def added_to(self, other):
    if isinstance(other, String):
      return String(self.value + other.value).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def multed_by(self, other):
    if isinstance(other, Number):
      return String(self.value * other.value).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def is_true(self):
    return len(self.value) > 0

  def copy(self):
    copy = String(self.value)
    copy.set_pos(self.pos_start, self.pos_end)
    copy.set_context(self.context)
    return copy

  def __str__(self):
    return self.value

  def __repr__(self):
    return f'"{self.value}"'

class List(Value):
  def __init__(self, elements):
    super().__init__()
    self.elements = elements

  def added_to(self, other):
    new_list = self.copy()
    new_list.elements.append(other)
    return new_list, None

  def subbed_by(self, other):
    if isinstance(other, Number):
      new_list = self.copy()
      try:
        new_list.elements.pop(other.value)
        return new_list, None
      except:
        return None, RTError(
          other.pos_start, other.pos_end,
          'Element at this index could not be removed from list because index is out of bounds',
          self.context
        )
    else:
      return None, Value.illegal_operation(self, other)

  def multed_by(self, other):
    if isinstance(other, List):
      new_list = self.copy()
      new_list.elements.extend(other.elements)
      return new_list, None
    else:
      return None, Value.illegal_operation(self, other)

  def dived_by(self, other):
    if isinstance(other, Number):
      try:
        return self.elements[other.value], None
      except:
        return None, RTError(
          other.pos_start, other.pos_end,
          'Element at this index could not be retrieved from list because index is out of bounds',
          self.context
        )
    else:
      return None, Value.illegal_operation(self, other)
      
  
  def copy(self):
    copy = List(self.elements)
    copy.set_pos(self.pos_start, self.pos_end)
    copy.set_context(self.context)
    return copy

  def __str__(self):
    return ", ".join([str(x) for x in self.elements])

  def __repr__(self):
    return f'[{", ".join([repr(x) for x in self.elements])}]'

class BaseFunction(Value):
  def __init__(self, name):
    super().__init__()
    self.name = name or "<anonymous>"

  def generate_new_context(self):
    new_context = Context(self.name, self.context, self.pos_start)
    new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
    return new_context

  def check_args(self, arg_names, args):
    res = RTResult()

    if len(args) > len(arg_names):
      return res.failure(RTError(
        self.pos_start, self.pos_end,
        f"{len(args) - len(arg_names)} too many args passed into {self}",
        self.context
      ))
    
    if len(args) < len(arg_names):
      return res.failure(RTError(
        self.pos_start, self.pos_end,
        f"{len(arg_names) - len(args)} too few args passed into {self}",
        self.context
      ))

    return res.success(None)

  def populate_args(self, arg_names, args, exec_ctx):
    for i in range(len(args)):
      arg_name = arg_names[i]
      arg_value = args[i]
      arg_value.set_context(exec_ctx)
      exec_ctx.symbol_table.set(arg_name, arg_value)

  def check_and_populate_args(self, arg_names, args, exec_ctx):
    res = RTResult()
    res.register(self.check_args(arg_names, args))
    if res.should_return(): return res
    self.populate_args(arg_names, args, exec_ctx)
    return res.success(None)

class Function(BaseFunction):
  def __init__(self, name, body_node, arg_names, should_auto_return):
    super().__init__(name)
    self.body_node = body_node
    self.arg_names = arg_names
    self.should_auto_return = should_auto_return

  def execute(self, args):
    res = RTResult()
    interpreter = Interpreter()
    exec_ctx = self.generate_new_context()

    res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
    if res.should_return(): return res

    value = res.register(interpreter.visit(self.body_node, exec_ctx))
    if res.should_return() and res.func_return_value == None: return res

    ret_value = (value if self.should_auto_return else None) or res.func_return_value or Number.null
    return res.success(ret_value)

  def copy(self):
    copy = Function(self.name, self.body_node, self.arg_names, self.should_auto_return)
    copy.set_context(self.context)
    copy.set_pos(self.pos_start, self.pos_end)
    return copy

  def __repr__(self):
    return f"<function {self.name}>"

class BuiltInFunction(BaseFunction):
  def __init__(self, name):
    super().__init__(name)

  def execute(self, args):
    res = RTResult()
    exec_ctx = self.generate_new_context()

    method_name = f'execute_{self.name}'
    method = getattr(self, method_name, self.no_visit_method)

    res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
    if res.should_return(): return res

    return_value = res.register(method(exec_ctx))
    if res.should_return(): return res
    return res.success(return_value)
  
  def no_visit_method(self, node, context):
    raise Exception(f'No execute_{self.name} method defined')

  def copy(self):
    copy = BuiltInFunction(self.name)
    copy.set_context(self.context)
    copy.set_pos(self.pos_start, self.pos_end)
    return copy

  def __repr__(self):
    return f"<built-in function {self.name}>"

  #####################################
  def execute_draw(self, exec_ctx):
    x_1 = exec_ctx.symbol_table.get('x1')
    x_2 = exec_ctx.symbol_table.get('x2')
    exp = String(exec_ctx.symbol_table.get('exp'))
    draw_exp(inputx=[x_1.to_realnum(),x_2.to_realnum()],inputy=exp.to_str())
    return RTResult().success(Number.null)
  execute_draw.arg_names = ['x1','x2','exp']

  def execute_print(self, exec_ctx):
    print(str(exec_ctx.symbol_table.get('value')))
    return RTResult().success(Number.null)
  execute_print.arg_names = ['value']
  
  def execute_print_ret(self, exec_ctx):
    return RTResult().success(String(str(exec_ctx.symbol_table.get('value'))))
  execute_print_ret.arg_names = ['value']
  
  def execute_input(self, exec_ctx):
    if exec_ctx.symbol_table.get('help'):
      text = input(String(str(exec_ctx.symbol_table.get('help')) + " "))
    else:
      text = input()
    return RTResult().success(String(text))
  execute_input.arg_names = ['help']

  def execute_input_int(self, exec_ctx):
    while True:
      text = input()
      try:
        number = int(text)
        break
      except ValueError:
        print(f"'{text}' must be an integer. Try again!")
    return RTResult().success(Number(number))
  execute_input_int.arg_names = []

  def execute_abs(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "ABS : Argument must be an Integer, Float",
        exec_ctx
      ))

    return RTResult().success(Number(abs(num.to_realnum())))
  execute_abs.arg_names = ["value"]

  def execute_flr(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "FLR : Argument must be an Integer, Float",
        exec_ctx
      ))

    return RTResult().success(Number(math.floor(num.to_realnum())))
  execute_flr.arg_names = ["value"]

  def execute_ceil(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "CEIL : Argument must be an Integer, Float",
        exec_ctx
      ))

    return RTResult().success(Number(math.ceil(num.to_realnum())))
  execute_ceil.arg_names = ["value"]

  def execute_log(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "LOG : Argument must be an Integer, Float",
        exec_ctx
      ))
      
    try:
      math.log10(num.to_realnum())
    except ValueError:
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "LOG : Out of domain.",
        exec_ctx
      ))

    if num.to_realnum() == 0:
      return RTResult().success(Number(- math.inf))
    elif math.log10(num.to_realnum()) % 1:
      return RTResult().success(Number(round(math.log10(num.to_realnum()),2)))
    else:
      return RTResult().success(Number(int(math.log10(num.to_realnum()))))
  execute_log.arg_names = ["value"]

  def execute_sqrt(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "SQRT : Argument must be an Integer, Float",
        exec_ctx
      ))

    try:
      square = math.sqrt(num.to_realnum())
    except:
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "SQRT : Argument must be an Integer, Float",
        exec_ctx
      ))

    if square % 1:
      return RTResult().success(String('SQRT(%s)' % round(num.to_realnum(),2)))
    else:
      return RTResult().success(Number(int(square)))
  execute_sqrt.arg_names = ["value"]

  def execute_sin(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "SIN : Argument must be an Integer",
        exec_ctx
      ))

    return RTResult().success(Number(round(math.sin(math.radians(num.to_realnum())),2)))
  execute_sin.arg_names = ["value"]

  def execute_cos(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "COS : Argument must be an Integer",
        exec_ctx
      ))

    return RTResult().success(Number(round(math.cos(math.radians(num.to_realnum())),2)))
  execute_cos.arg_names = ["value"]

  def execute_cot(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "COT : Argument must be an Integer",
        exec_ctx
      ))

    return RTResult().success(Number(round((1/math.tan(math.radians(num.to_realnum()))),2)))
  execute_cot.arg_names = ["value"]

  def execute_tan(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "TAN : Argument must be an Integer",
        exec_ctx
      ))

    return RTResult().success(Number(round(math.tan(math.radians(num.to_realnum())),2)))
  execute_tan.arg_names = ["value"]

  def execute_asin(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "ASIN : Argument must be an Integer",
        exec_ctx
      ))

    return RTResult().success(Number(round(math.asin(math.radians(num.to_realnum())),2)))
  execute_asin.arg_names = ["value"]

  def execute_acos(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "ACOS : Argument must be an Integer",
        exec_ctx
      ))

    return RTResult().success(Number(round(math.acos(math.radians(num.to_realnum())),2)))
  execute_acos.arg_names = ["value"]

  def execute_acot(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "ACOT : Argument must be an Integer",
        exec_ctx
      ))

    return RTResult().success(Number(round((math.pi/2) - math.atan(math.radians(num.to_realnum())),2)))
  execute_acot.arg_names = ["value"]

  def execute_atan(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "ATAN : Argument must be an Integer",
        exec_ctx
      ))

    return RTResult().success(Number(round(math.atan(math.radians(num.to_realnum())),2)))
  execute_atan.arg_names = ["value"]

  def execute_len(self, exec_ctx):
    list_ = exec_ctx.symbol_table.get("list")

    if not isinstance(list_, List):
      return RTResult().failure(RTError(
        self.pos_start, self.pos_end,
        "Argument must be list",
        exec_ctx
      ))

    return RTResult().success(Number(len(list_.elements)))
  execute_len.arg_names = ["list"]

  def execute_run(self, exec_ctx):
    fn = exec_ctx.symbol_table.get("fn")

    if not isinstance(fn, String):
      return RTResult().failure(RTError(
        self.pos_start, self.pos_end,
        "Second argument must be string",
        exec_ctx
      ))

    fn = fn.value

    try:
      with open(fn, "r") as f:
        script = f.read()
    except Exception as e:
      return RTResult().failure(RTError(
        self.pos_start, self.pos_end,
        f"Failed to load script \"{fn}\"\n" + str(e),
        exec_ctx
      ))

    _, error = run(fn, script)
    
    if error:
      return RTResult().failure(RTError(
        self.pos_start, self.pos_end,
        f"Failed to finish executing script \"{fn}\"\n" +
        error.as_string(),
        exec_ctx
      ))

    return RTResult().success(Number.null)
  execute_run.arg_names = ["fn"]


BuiltInFunction.abs         = BuiltInFunction("abs")
BuiltInFunction.flr         = BuiltInFunction("flr")
BuiltInFunction.ceil        = BuiltInFunction("ceil")
BuiltInFunction.log         = BuiltInFunction("log")
BuiltInFunction.sqrt        = BuiltInFunction("sqrt")
BuiltInFunction.sin         = BuiltInFunction("sin")
BuiltInFunction.cos         = BuiltInFunction("cos")
BuiltInFunction.cot         = BuiltInFunction("cot")
BuiltInFunction.tan         = BuiltInFunction("tan")
BuiltInFunction.asin        = BuiltInFunction("asin")
BuiltInFunction.acos        = BuiltInFunction("acos")
BuiltInFunction.acot        = BuiltInFunction("acot")
BuiltInFunction.atan        = BuiltInFunction("atan")
BuiltInFunction.draw        = BuiltInFunction("draw")
BuiltInFunction.print       = BuiltInFunction("print")
BuiltInFunction.print_ret   = BuiltInFunction("print_ret")
BuiltInFunction.input       = BuiltInFunction("input")
BuiltInFunction.input_int   = BuiltInFunction("input_int")
BuiltInFunction.run					= BuiltInFunction("run")

# INTERPRETER
class Interpreter:
  def visit(self, node, context):
    method_name = f'visit_{type(node).__name__}'
    method = getattr(self, method_name, self.no_visit_method)
    return method(node, context)

  def no_visit_method(self, node, context):
    raise Exception(f'No visit_{type(node).__name__} method defined')

  ###################################

  def visit_NumberNode(self, node, context):
    return RTResult().success(
      Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
    )

  def visit_StringNode(self, node, context):
    return RTResult().success(
      String(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
    )

  def visit_ListNode(self, node, context):
    res = RTResult()
    elements = []

    for element_node in node.element_nodes:
      elements.append(res.register(self.visit(element_node, context)))
      if res.should_return(): return res

    return res.success(
      List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
    )

  def visit_VarAccessNode(self, node, context):
    res = RTResult()
    var_name = node.var_name_tok.value
    value = context.symbol_table.get(var_name)

    if var_name == 'x' and not value:
      return res.failure(RTError(
              node.pos_start, node.pos_end,
              f"'{var_name}' is wtf",
              context
            ))

    if not value:
      return res.failure(RTError(
        node.pos_start, node.pos_end,
        f"'{var_name}' is not defined",
        context
      ))

    value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
    return res.success(value)

  def visit_VarAssignNode(self, node, context):
    res = RTResult()
    var_name = node.var_name_tok.value
    value = res.register(self.visit(node.value_node, context))
    if res.should_return(): return res

    context.symbol_table.set(var_name, value)
    return res.success(value)

  def visit_BinOpNode(self, node, context):
    res = RTResult()
    left = res.register(self.visit(node.left_node, context))
    if res.should_return(): return res
    right = res.register(self.visit(node.right_node, context))
    if res.should_return(): return res

    if node.op_tok.type == TT_PLUS:
      result, error = left.added_to(right)
    elif node.op_tok.type == TT_MINUS:
      result, error = left.subbed_by(right)
    elif node.op_tok.type == TT_MUL:
      result, error = left.multed_by(right)
    elif node.op_tok.type == TT_DIV:
      result, error = left.dived_by(right)
    elif node.op_tok.type == TT_MOD:
      result, error = left.moded_by(right)
    elif node.op_tok.type == TT_POW:
      result, error = left.powed_by(right)
    elif node.op_tok.type == TT_EE:
      result, error = left.get_comparison_eq(right)
    elif node.op_tok.type == TT_NE:
      result, error = left.get_comparison_ne(right)
    elif node.op_tok.type == TT_LT:
      result, error = left.get_comparison_lt(right)
    elif node.op_tok.type == TT_GT:
      result, error = left.get_comparison_gt(right)
    elif node.op_tok.type == TT_LTE:
      result, error = left.get_comparison_lte(right)
    elif node.op_tok.type == TT_GTE:
      result, error = left.get_comparison_gte(right)
    elif node.op_tok.matches(TT_KEYWORD, 'AND'):
      result, error = left.anded_by(right)
    elif node.op_tok.matches(TT_KEYWORD, 'OR'):
      result, error = left.ored_by(right)

    if error:
      return res.failure(error)
    else:
      return res.success(result.set_pos(node.pos_start, node.pos_end))

  def visit_UnaryOpNode(self, node, context):
    res = RTResult()
    number = res.register(self.visit(node.node, context))
    if res.should_return(): return res

    error = None

    if node.op_tok.type == TT_MINUS:
      number, error = number.multed_by(Number(-1))
    elif node.op_tok.matches(TT_KEYWORD, 'NOT'):
      number, error = number.notted()

    if error:
      return res.failure(error)
    else:
      return res.success(number.set_pos(node.pos_start, node.pos_end))

  def visit_CallNode(self, node, context):
    res = RTResult()
    args = []

    value_to_call = res.register(self.visit(node.node_to_call, context))
    if res.should_return(): return res
    value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

    for arg_node in node.arg_nodes:
      args.append(res.register(self.visit(arg_node, context)))
      if res.should_return(): return res

    return_value = res.register(value_to_call.execute(args))
    if res.should_return(): return res
    return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
    return res.success(return_value)

# RUN
global_symbol_table = SymbolTable()
global_symbol_table.set("NULL", Number.null)
global_symbol_table.set("FALSE", Number.false)
global_symbol_table.set("TRUE", Number.true)
global_symbol_table.set("MATH_PI", Number.math_PI)
global_symbol_table.set("e", Number.math_E)
global_symbol_table.set("ABS", BuiltInFunction.abs)
global_symbol_table.set("FLR", BuiltInFunction.flr)
global_symbol_table.set("CEIL", BuiltInFunction.ceil)
global_symbol_table.set("LOG", BuiltInFunction.log)
global_symbol_table.set("SQRT", BuiltInFunction.sqrt)
global_symbol_table.set("SIN", BuiltInFunction.sin)
global_symbol_table.set("COS", BuiltInFunction.cos)
global_symbol_table.set("COT", BuiltInFunction.cot)
global_symbol_table.set("TAN", BuiltInFunction.tan)
global_symbol_table.set("ASIN", BuiltInFunction.asin)
global_symbol_table.set("ACOS", BuiltInFunction.acos)
global_symbol_table.set("ACOT", BuiltInFunction.acot)
global_symbol_table.set("ATAN", BuiltInFunction.atan)
global_symbol_table.set("DRAW", BuiltInFunction.draw)
global_symbol_table.set("PRINT", BuiltInFunction.print)
global_symbol_table.set("PRINT_RET", BuiltInFunction.print_ret)
global_symbol_table.set("INPUT", BuiltInFunction.input)
global_symbol_table.set("INPUT_INT", BuiltInFunction.input_int)
global_symbol_table.set("RUN", BuiltInFunction.run)

def run(fn, text):
  # Generate tokens
  lexer = Lexer(fn, text)
  tokens, error = lexer.make_tokens()
  if error: return None, error
  
  # Generate AST
  parser = Parser(tokens)
  ast = parser.parse()
  if ast.error: return None, ast.error

  # Run program
  interpreter = Interpreter()
  context = Context('<program>')
  context.symbol_table = global_symbol_table
  result = interpreter.visit(ast.node, context)

  return result.value, result.error
