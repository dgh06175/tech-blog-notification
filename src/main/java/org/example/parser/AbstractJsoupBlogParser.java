package org.example.parser;

import java.util.ArrayList;
import java.util.List;
import org.example.model.Article;
import org.example.model.Articles;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public abstract class AbstractJsoupBlogParser implements ParserStrategy {
    @Override
    public Articles parse(String url, String blogName) {
        List<Article> articles = new ArrayList<>();
        try {
            Document document = Jsoup.connect(url).get();
            Elements items = document.select(getItemTagName());
            for (Element item : items) {
                articles.add(parseElement(item));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return new Articles(articles, blogName);
    }

    /// MARK: 블로그 게시글의 태그
    protected abstract String getItemTagName();

    /// MARK: 블로그 게시글 하나의 정보들 파싱해서 반환
    protected abstract Article parseElement(Element element);
}
