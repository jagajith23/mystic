package JMystic.mystic;

import java.util.HashMap;
import java.util.Map;

/**
 * Environment
 */
public class Environment {
    final Environment enclosing;
    private final Map<String, Object> values = new HashMap<>();

    Environment() {
        enclosing = null;
    }

    Environment(Environment enclosing) {
        this.enclosing = enclosing;
    }

    void define(String name, Object value) {
        values.put(name, value);
    }

    Object get(Token name) {
        if (values.containsKey(name.lexeme))
            return values.get(name.lexeme);

        if (enclosing != null)
            return enclosing.get(name);

        throw new RuntimeError(name, "Undefined variable '" + name.lexeme + "'.");
    }

    Object getAt(int dist, String name) {
        return ancestor(dist).values.get(name);
    }

    void assign(Token name, Object value) {
        if (values.containsKey(name.lexeme)) {
            values.put(name.lexeme, value);
            return;
        }

        if (enclosing != null) {
            enclosing.assign(name, value);
            return;
        }

        throw new RuntimeError(name, "Undefined variable '" + name.lexeme + "'.");
    }

    void assignAt(int dist, Token name, Object value) {
        ancestor(dist).values.put(name.lexeme, value);
    }

    Environment ancestor(int dist) {
        Environment env = this;
        for (int i = 0; i < dist; i++)
            env = env.enclosing;

        return env;
    }
}