package org.example.parser;

import java.util.List;
import java.util.Map;

public interface ParserStrategy {
    List<Map<String, String>> parse(String url);
}
