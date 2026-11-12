import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.lang.reflect.Array;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;
import java.nio.charset.StandardCharsets;

/** Small dependency-free adapter for the primitive/string/array Java solutions. */
public class LocalRunner {
    public static void main(String[] options) throws Exception {
        System.setOut(new PrintStream(System.out, true, StandardCharsets.UTF_8));
        Class<?> solutionClass = Class.forName(options[0]);
        String methodName = options[1];
        int outputArg = Integer.parseInt(options[2]);
        List<Object> inputs = new ArrayList<>();
        BufferedReader stdin = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
        for (String line; (line = stdin.readLine()) != null;) {
            if (!line.isBlank()) inputs.add(new Json(line).parse());
        }
        Method target = null;
        for (Method method : solutionClass.getDeclaredMethods()) {
            if (method.getName().equals(methodName) && method.getParameterCount() == inputs.size()) {
                if (target != null) throw new IllegalArgumentException("Ambiguous overloaded method: " + methodName);
                target = method;
            }
        }
        if (target == null) throw new IllegalArgumentException("No matching method: " + methodName);
        Object[] args = new Object[inputs.size()];
        for (int i = 0; i < args.length; i++) {
            args[i] = convert(inputs.get(i), target.getParameterTypes()[i]);
        }
        Object result;
        try {
            result = target.invoke(solutionClass.getDeclaredConstructor().newInstance(), args);
        } catch (InvocationTargetException exception) {
            throw new RuntimeException("Solution threw an exception", exception.getCause());
        }
        System.out.println("\noutput: " + Json.stringify(outputArg >= 0 ? args[outputArg] : result));
    }

    private static Object convert(Object value, Class<?> type) {
        if (value == null) {
            if (type.isPrimitive()) throw new IllegalArgumentException("null for primitive input");
            return null;
        }
        if (type.isArray()) {
            if (!(value instanceof List<?> list)) throw new IllegalArgumentException("Expected JSON array");
            Object result = Array.newInstance(type.componentType(), list.size());
            for (int i = 0; i < list.size(); i++) Array.set(result, i, convert(list.get(i), type.componentType()));
            return result;
        }
        if (type == int.class || type == Integer.class) return Math.toIntExact(((Number) value).longValue());
        if (type == long.class || type == Long.class) return ((Number) value).longValue();
        if (type == double.class || type == Double.class) return ((Number) value).doubleValue();
        if (type == float.class || type == Float.class) return ((Number) value).floatValue();
        if (type == boolean.class || type == Boolean.class) return (Boolean) value;
        if (type == char.class || type == Character.class) {
            if (!(value instanceof String text) || text.length() != 1) {
                throw new IllegalArgumentException("Expected single-character string");
            }
            return text.charAt(0);
        }
        if (type == String.class) return (String) value;
        throw new IllegalArgumentException("Unsupported Java input type: " + type.getTypeName());
    }

    private static final class Json {
        private final String text;
        private int index;

        Json(String text) { this.text = text; }

        Object parse() {
            Object result = value();
            whitespace();
            if (index != text.length()) throw invalid();
            return result;
        }

        private IllegalArgumentException invalid() {
            return new IllegalArgumentException("Invalid JSON at offset " + index + ": " + text);
        }

        private void whitespace() {
            while (index < text.length() && Character.isWhitespace(text.charAt(index))) index++;
        }

        private Object value() {
            whitespace();
            if (index >= text.length()) throw invalid();
            char ch = text.charAt(index);
            if (ch == '"') return string();
            if (ch == '[') {
                index++;
                List<Object> result = new ArrayList<>();
                whitespace();
                if (index < text.length() && text.charAt(index) == ']') { index++; return result; }
                while (true) {
                    result.add(value());
                    whitespace();
                    if (index >= text.length()) throw invalid();
                    char delimiter = text.charAt(index++);
                    if (delimiter == ']') return result;
                    if (delimiter != ',') throw invalid();
                }
            }
            for (String literal : new String[]{"true", "false", "null"}) {
                if (text.startsWith(literal, index)) {
                    index += literal.length();
                    return literal.equals("null") ? null : Boolean.valueOf(literal);
                }
            }
            int start = index;
            while (index < text.length() && "-+0123456789.eE".indexOf(text.charAt(index)) >= 0) index++;
            String number = text.substring(start, index);
            if (!number.matches("-?(0|[1-9][0-9]*)(\\.[0-9]+)?([eE][+-]?[0-9]+)?")) throw invalid();
            if (number.contains(".") || number.contains("e") || number.contains("E")) return Double.valueOf(number);
            return Long.valueOf(number);
        }

        private String string() {
            index++;
            StringBuilder result = new StringBuilder();
            while (index < text.length()) {
                char ch = text.charAt(index++);
                if (ch == '"') return result.toString();
                if (ch < 0x20) throw invalid();
                if (ch != '\\') { result.append(ch); continue; }
                if (index >= text.length()) throw invalid();
                ch = text.charAt(index++);
                switch (ch) {
                    case '"', '\\', '/' -> result.append(ch);
                    case 'b' -> result.append('\b');
                    case 'f' -> result.append('\f');
                    case 'n' -> result.append('\n');
                    case 'r' -> result.append('\r');
                    case 't' -> result.append('\t');
                    case 'u' -> {
                        if (index + 4 > text.length()) throw invalid();
                        result.append((char) Integer.parseInt(text.substring(index, index + 4), 16));
                        index += 4;
                    }
                    default -> throw invalid();
                }
            }
            throw invalid();
        }

        static String stringify(Object value) {
            if (value == null) return "null";
            if (value instanceof String || value instanceof Character) {
                StringBuilder result = new StringBuilder("\"");
                for (char ch : value.toString().toCharArray()) {
                    switch (ch) {
                        case '"' -> result.append("\\\"");
                        case '\\' -> result.append("\\\\");
                        case '\n' -> result.append("\\n");
                        case '\r' -> result.append("\\r");
                        case '\t' -> result.append("\\t");
                        default -> {
                            if (ch < 0x20) result.append(String.format("\\u%04x", (int) ch));
                            else result.append(ch);
                        }
                    }
                }
                return result.append('"').toString();
            }
            if (value instanceof Double number && !Double.isFinite(number)) {
                throw new IllegalArgumentException("Non-finite output");
            }
            if (value instanceof Number || value instanceof Boolean) return value.toString();
            List<String> items = new ArrayList<>();
            if (value instanceof Iterable<?> iterable) {
                for (Object item : iterable) items.add(stringify(item));
            } else if (value.getClass().isArray()) {
                for (int i = 0; i < Array.getLength(value); i++) items.add(stringify(Array.get(value, i)));
            } else {
                throw new IllegalArgumentException("Unsupported output type: " + value.getClass());
            }
            return "[" + String.join(",", items) + "]";
        }
    }
}
