package JMystic.mystic;

import java.util.List;

/**
 * MysticCallable
 */
interface MysticCallable {
    int arity();

    Object call(Interpreter interpreter, List<Object> arguments);

}