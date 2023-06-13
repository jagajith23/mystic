package JMystic.mystic;

import java.util.List;

/**
 * Interpreter
 */
public class Interpreter implements Expr.Visitor<Object>, Stmt.Visitor<Void> {
    private Environment env = new Environment();

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

    private void executeBlock(List<Stmt> statements, Environment env) {
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
    public Void visitBlockStmt(Stmt.Block stmt) {
        executeBlock(stmt.statements, new Environment(env));
        return null;
    }

    @Override
    public Void visitExpressionStmt(Stmt.Expression stmt) {
        Object value = evaluate(stmt.expression);
        System.out.println(stringify(value));
        return null;
    }

    @Override
    public Void visitIfStmt(Stmt.If Stmt) {
        if (isTruthy(evaluate(Stmt.condition))) {
            execute(Stmt.thenBranch);
        } else if (Stmt.elseBranch != null) {
            execute(Stmt.elseBranch);
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
        env.assign(expr.name, value);
        return value;
    }

    @Override
    public Object visitVariableExpr(Expr.Variable expr) {
        Object value = env.get(expr.name);

        if (value == null)
            throw new RuntimeError(expr.name, "Undefined variable '" + expr.name.lexeme + "'" + " at line "
                    + expr.name.line + ".");

        return value;
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