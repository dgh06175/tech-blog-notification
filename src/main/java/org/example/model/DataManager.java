package org.example.model;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;

public class DataManager {
    // 상수 선언
    private static final String JSON_LOAD_FAILURE = "JSON 데이터 불러오기 실패: ";
    private static final String JSON_SAVE_FAILURE = "JSON 데이터 저장 실패: ";
    private static final String DATA_SAVED_TO = "데이터 %s 에 저장됨%n";
    private static final String PAST_DATA_FOLDER = "/pastData/";
    private static final String LINK_DATA_SUFFIX = "_link_data.json";

    /**
     * JSON 파일에서 데이터를 읽는다.
     *
     * @param blogName 읽을 파일 블로그 이름
     * @return 파일에서 읽은 데이터 목록
     */
    public Articles readArticlesFromJsonFile(String blogName) {
        ObjectMapper mapper = new ObjectMapper();
        try {
            List<Map<String, String>> value = mapper.readValue(new File(getFileName(blogName)), new TypeReference<>() {
            });
            return new Articles(value, blogName);
        } catch (IOException e) {
            e.printStackTrace();
            System.err.println(JSON_LOAD_FAILURE + e.getMessage());
            return null;
        }
    }

    /**
     * 데이터를 JSON 형식으로 파일에 저장합니다.
     *
     * @param articles 변환할 데이터 목록
     */
    public void saveArticlesToJsonFile(Articles articles) {
        String filename = getFileName(articles.blogName);
        ObjectMapper mapper = new ObjectMapper();
        try {
            mapper.enable(SerializationFeature.INDENT_OUTPUT);
            mapper.writeValue(new File(filename), articles.getArticles());
            System.out.printf(DATA_SAVED_TO, filename);
        } catch (IOException e) {
            System.err.println(JSON_SAVE_FAILURE + e.getMessage());
        }
    }

    private String getFileName(String blogName) {
        String rootPath = System.getProperty("user.dir");
        return rootPath + PAST_DATA_FOLDER + blogName + LINK_DATA_SUFFIX;
    }
}
