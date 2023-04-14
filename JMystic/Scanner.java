package JMystic;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static JMystic.TokenType.*;

/**
 * Scanner
 */
public class Scanner {
    private final String source;
    private final List<Token> tokens = new ArrayList<>();
    private int start = 0;
    private int current = 0;
    private int line = 1;
    private final int sourceLen;
    private static final Map<String, TokenType> keywords;

    static {
        keywords = new HashMap<>();
        keywords.put("and", AND);
        keywords.put("class", CLASS);
        keywords.put("else", ELSE);
        keywords.put("false", FALSE);
        keywords.put("for", FOR);
        keywords.put("fun", FUN);
        keywords.put("if", IF);
        keywords.put("nil", NIL);
        keywords.put("or", OR);
        keywords.put("print", PRINT);
        keywords.put("return", RETURN);
        keywords.put("parent", PARENT);
        keywords.put("this", THIS);
        keywords.put("true", TRUE);
        keywords.put("store", STORE);
        keywords.put("while", WHILE);
    }

    Scanner(String source) {
        this.source = source;
        sourceLen = source.length();
    }

    List<Token> scanTokens() {
        while (!isAtEnd()) {
            // We are at the beginning of the next lexeme.
            start = current;
            scanToken();
        }

        tokens.add(new Token(EOF, "", null, line));
        return tokens;
    }

    private boolean isAtEnd() {
        return current >= sourceLen;
    }

    private void scanToken() {
        char c = advance();

        if (c == '(')
            addToken(LEFT_PAREN);
        else if (c == ')')
            addToken(RIGHT_PAREN);
        else if (c == '{')
            addToken(LEFT_BRACE);
        else if (c == '}')
            addToken(RIGHT_BRACE);
        else if (c == ',')
            addToken(COMMA);
        else if (c == '.')
            addToken(DOT);
        else if (c == '-')
            addToken(MINUS);
        else if (c == '+')
            addToken(PLUS);
        else if (c == ';')
            addToken(SEMICOLON);
        else if (c == '*')
            addToken(STAR);
        else if (c == '!')
            addToken(match('=') ? BANG_EQUAL : BANG);
        else if (c == '=')
            addToken(match('=') ? EQUAL_EQUAL : EQUAL);
        else if (c == '<')
            addToken(match('=') ? LESS_EQUAL : LESS);
        else if (c == '>')
            addToken(match('=') ? GREATER_EQUAL : GREATER);
        else if (c == '/')
            if (match('/')) {
                // A comment goes until the end of the line.
                while (peek() != '\n' && !isAtEnd())
                    advance();
            } else {
                addToken(SLASH);
            }
        else if (c == ' ' || c == '\r' || c == '\t')
            ;
        else if (c == '\n')
            line++;
        else if (c == '"')
            string();
        else if (isDigit(c))
            number();
        else if (isAlpha(c))
            indentifier();
        else
            Mystic.error(line, "Unexpected character.");
    }

    private void indentifier() {
        while (isAlphaNumeric(peek()))
            advance();

        String text = source.substring(start, current);
        TokenType type = keywords.get(text);
        if (type == null)
            type = IDENTIFIER;
        addToken(type);
    }

    private boolean isAlpha(char c) {
        return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '_';
    }

    private boolean isAlphaNumeric(char c) {
        return isAlpha(c) || isDigit(c);
    }

    private void number() {
        while (isDigit(peek()))
            advance();

        // Look for a fractional part.
        if (peek() == '.' && isDigit(peekNext())) {
            // Consume the "."
            advance();

            while (isDigit(peek()))
                advance();
        }

        addToken(NUMBER, parseDouble(source.substring(start, current)));
    }

    private char peekNext() {
        if (current + 1 >= sourceLen)
            return '\0';
        return source.charAt(current + 1);
    }

    private boolean isDigit(char c) {
        return c >= '0' && c <= '9';
    }

    private void string() {
        while (peek() != '"' && !isAtEnd()) {
            if (peek() == '\n')
                line++;
            advance();
        }

        if (isAtEnd()) {
            Mystic.error(line, "Unterminated string.");
            return;
        }

        // The closing ".
        advance();

        String value = source.substring(start + 1, current - 1);
        addToken(STRING, value);
    }

    private char peek() {
        if (isAtEnd())
            return '\0';
        return source.charAt(current);
    }

    private boolean match(char expected) {
        if (isAtEnd())
            return false;
        if (source.charAt(current) != expected)
            return false;

        current++;
        return true;
    }

    private char advance() {
        return source.charAt(current++);
    }

    private void addToken(TokenType type) {
        addToken(type, null);
    }

    private void addToken(TokenType type, Object literal) {
        String text = source.substring(start, current);
        tokens.add(new Token(type, text, literal, line));
    }

    private double parseDouble(String lexeme) {
        int integerPart = 0;
        int fractionalPart = 0;
        boolean isFraction = false;
        double fractionalMultiplier = 1;

        lexeme = lexeme.strip();

        for (char c : lexeme.toCharArray()) {
            if (c == '.') {
                if (isFraction == true) {
                    throw new NumberFormatException("Invalid lexeme: " + lexeme);
                }
                isFraction = true;
                continue;
            }

            if (!isFraction) {
                integerPart *= 10;
                integerPart += c - '0';
            } else {
                fractionalMultiplier *= 0.1;
                fractionalPart = fractionalPart * 10 + (c - '0');
            }
        }

        return integerPart + fractionalPart * fractionalMultiplier;

    }
}