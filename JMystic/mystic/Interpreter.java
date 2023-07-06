package JMystic.mystic;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Interpreter
 */
public class Interpreter implements Expr.Visitor<Object>, Stmt.Visitor<Void> {
    final Environment globals = new Environment();
    private Environment env = globals;
    private final Map<Expr, Integer> locals = new HashMap<>();

    private static class BreakException extends RuntimeException {
    }

    private static class ContinueException extends RuntimeException {
    }

    Interpreter() {
        globals.define("clock", new MysticCallable() {
            @Override
            public int arity() {
                return 0;
            }

            @Override
            public Object call(Interpreter interpreter, List<Object> arguments) {
                return (double) System.currentTimeMillis() / 1000.0;
            }

            @Override
            public String toString() {
                return "<native fn>";
            }
        });
    }

    void interpret(List<Stmt> statements) {
        try {
            for (Stmt statement : statements) {
                execute(statement);
            }
        } catch (RuntimeError e) {
            Mystic.runtimeError(e);
        }
    }

    // ------- Helper Methods ------- //

    private void execute(Stmt stmt) {
        stmt.accept(this);
    }

    void resolve(Expr expr, int depth) {
        locals.put(expr, depth);
    }

    void executeBlock(List<Stmt> statements, Environment env) {
        Environment previous = this.env;

        try {
            this.env = env;

            for (Stmt statement : statements) {
                execute(statement);
            }
        } finally {
            this.env = previous;
        }
    }

    private String stringify(Object object) {
        if (object == null)
            return "nil";

        if (object instanceof Double) {
            String text = object.toString();
            if (text.endsWith(".0")) {
                text = text.substring(0, text.length() - 2);
            }
            return text;
        }

        return object.toString();
    }

    private Object evaluate(Expr expr) {
        return expr.accept(this);
    }

    private boolean isTruthy(Object object) {
        if (object == null) {
            return false;
        }

        if (object instanceof Boolean) {
            return (boolean) object;
        }

        if (object instanceof Double) {
            return (double) object != 0;
        }

        if (object instanceof String) {
            return !((String) object).isEmpty();
        }

        if (object instanceof Character) {
            return (char) object != '\0';
        }

        return true;
    }

    private void checkNumberOperand(Token operator, Object operand) {
        if (operand instanceof Double)
            return;
        throw new RuntimeError(operator, "Operand must be a number.");
    }

    private void checkNumberOperands(Token operator, Object left, Object right) {
        if (left instanceof Double && right instanceof Double)
            return;
        throw new RuntimeError(operator, "Operands must be numbers.");
    }

    private Boolean isEqual(Object a, Object b) {
        if (a == null && b == null)
            return true;
        if (a == null)
            return false;

        return a.equals(b);
    }

    // ------- Visitor Methods ------- //
    @Override
    public Void visitFunctionStmt(Stmt.Function stmt) {
        MysticFunction function = new MysticFunction(stmt, env);
        env.define(stmt.name.lexeme, function);
        return null;
    }

    @Override
    public Void visitBlockStmt(Stmt.Block stmt) {
        executeBlock(stmt.statements, new Environment(env));
        return null;
    }

    @Override
    public Void visitExpressionStmt(Stmt.Expression stmt) {
        Object value = evaluate(stmt.expression);
        if (Mystic.isRepl)
            // if (value != null)
            System.out.println(stringify(value));
        return null;
    }

    @Override
    public Void visitIfStmt(Stmt.If stmt) {
        if (isTruthy(evaluate(stmt.condition))) {
            execute(stmt.thenBranch);
        } else if (stmt.elseBranch != null) {
            execute(stmt.elseBranch);
        }
        return null;
    }

    @Override
    public Void visitBreakStmt(Stmt.Break stmt) {
        throw new BreakException();
    }

    @Override
    public Void visitContinueStmt(Stmt.Continue stmt) {
        throw new ContinueException();
    }

    @Override
    public Void visitWhileStmt(Stmt.While stmt) {
        try {
            while (isTruthy(evaluate(stmt.condition))) {
                execute(stmt.body);
            }
        } catch (BreakException e) {
            // Eat 5 star, do nothing
        } catch (ContinueException e) {
            visitWhileStmt(stmt);
        }
        return null;
    }

    @Override
    public Void visitPrintStmt(Stmt.Print stmt) {
        Object value = evaluate(stmt.expression);
        System.out.println(stringify(value));
        return null;
    }

    @Override
    public Void visitReturnStmt(Stmt.Return stmt) {
        Object value = null;
        if (stmt.value != null)
            value = evaluate(stmt.value);
        throw new Return(value);
    }

    @Override
    public Void visitVarStmt(Stmt.Var stmt) {
        Object value = null;
        if (stmt.initializer != null)
            value = evaluate(stmt.initializer);

        env.define(stmt.name.lexeme, value);
        return null;
    }

    @Override
    public Object visitAssignExpr(Expr.Assign expr) {
        Object value = evaluate(expr.value);

        Integer dist = locals.get(expr);
        if (dist != null)
            env.assignAt(dist, expr.name, value);
        else
            globals.assign(expr.name, value);

        return value;
    }

    @Override
    public Object visitVariableExpr(Expr.Variable expr) {

        // if (value == null)
        // throw new RuntimeError(expr.name, "Undefined variable '" + expr.name.lexeme +
        // "'" + " at line "
        // + expr.name.line + ".");

        return lookUpVariable(expr.name, expr);
    }

    private Object lookUpVariable(Token name, Expr expr) {
        Integer dist = locals.get(expr);

        if (dist != null)
            return env.getAt(dist, name.lexeme);
        else
            return globals.get(name);
    }

    @Override
    public Object visitLiteralExpr(Expr.Literal expr) {
        return expr.value;
    }

    @Override
    public Object visitLogicalExpr(Expr.Logical expr) {
        Object left = evaluate(expr.left);

        if (expr.operator.type == TokenType.OR) {
            if (isTruthy(left))
                return left;
        } else {
            if (!isTruthy(left))
                return left;
        }

        return evaluate(expr.right);
    }

    @Override
    public Object visitGroupingExpr(Expr.Grouping expr) {
        return evaluate(expr.expression);
    }

    @Override
    public Object visitTernaryExpr(Expr.Ternary expr) {
        Object condition = evaluate(expr.condition);

        if (isTruthy(condition))
            return evaluate(expr.trueExpr);
        return evaluate(expr.falseExpr);
    }

    @Override
    public Object visitBinaryExpr(Expr.Binary expr) {
        Object left = evaluate(expr.left);
        Object right = evaluate(expr.right);

        TokenType operatorType = expr.operator.type;

        if (operatorType == TokenType.MINUS) {
            checkNumberOperands(expr.operator, left, right);
            return (double) left - (double) right;
        } else if (operatorType == TokenType.SLASH) {
            checkNumberOperands(expr.operator, left, right);
            if ((double) right == 0)
                throw new RuntimeError(expr.operator, "Cannot divide by zero.");
            return (double) left / (double) right;
        } else if (operatorType == TokenType.STAR) {
            checkNumberOperands(expr.operator, left, right);
            return (double) left * (double) right;
        } else if (operatorType == TokenType.PLUS) {
            if (left instanceof Double && right instanceof Double)
                return (double) left + (double) right;
            if (left instanceof String && right instanceof String)
                return (String) left + (String) right;
            if (left instanceof String && right instanceof Double)
                return (String) left + stringify(right);
            if (left instanceof Double && right instanceof String)
                return stringify(left) + (String) right;
        } else if (operatorType == TokenType.GREATER) {
            checkNumberOperands(expr.operator, left, right);
            return (double) left > (double) right;
        } else if (operatorType == TokenType.GREATER_EQUAL) {
            checkNumberOperands(expr.operator, left, right);
            return (double) left >= (double) right;
        } else if (operatorType == TokenType.LESS) {
            checkNumberOperands(expr.operator, left, right);
            return (double) left < (double) right;
        } else if (operatorType == TokenType.LESS_EQUAL) {
            checkNumberOperands(expr.operator, left, right);
            return (double) left <= (double) right;
        } else if (operatorType == TokenType.BANG_EQUAL) {
            checkNumberOperands(expr.operator, left, right);
            return !isEqual(left, right);
        } else if (operatorType == TokenType.EQUAL_EQUAL) {
            checkNumberOperands(expr.operator, left, right);
            return isEqual(left, right);
        }

        return null;
    }

    @Override
    public Object visitCallExpr(Expr.Call expr) {
        Object callee = evaluate(expr.callee);

        List<Object> arguments = new ArrayList<>();
        for (Expr argument : expr.arguments)
            arguments.add(evaluate(argument));

        if (!(callee instanceof MysticCallable))
            throw new RuntimeError(expr.paren, "Can only call functions and classes.");

        MysticCallable function = (MysticCallable) callee;

        if (arguments.size() != function.arity())
            throw new RuntimeError(expr.paren, "Expected " + function.arity() + " arguments but got " + arguments.size()
                    + ".");

        return function.call(this, arguments);
    }

    @Override
    public Object visitUnaryExpr(Expr.Unary expr) {
        Object right = evaluate(expr.right);

        TokenType operatorType = expr.operator.type;

        if (operatorType == TokenType.MINUS) {
            checkNumberOperand(expr.operator, right);
            return -(double) right;
        } else if (operatorType == TokenType.BANG) {
            return !isTruthy(right);
        }

        return null;
    }
}