package com.dgh06175.techblognotificationsscrapper.service;


import com.dgh06175.techblognotificationsscrapper.config.BlogConfig;
import com.dgh06175.techblognotificationsscrapper.config.html.Toss;
import com.dgh06175.techblognotificationsscrapper.config.rss.Kakao;
import com.dgh06175.techblognotificationsscrapper.config.rss.Woowahan;
import com.dgh06175.techblognotificationsscrapper.domain.Post;
import com.dgh06175.techblognotificationsscrapper.exception.*;
import com.dgh06175.techblognotificationsscrapper.repository.PostRepository;
import java.io.IOException;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;
import lombok.RequiredArgsConstructor;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class PostService {
    private static final Logger logger = LoggerFactory.getLogger(PostService.class.getName());

    private final PostRepository postRepository;

    public List<BlogConfig> getBlogConfigs() {
        List<BlogConfig> tmpConfigs = new ArrayList<>();
        tmpConfigs.add(new Toss());
        tmpConfigs.add(new Woowahan());
        tmpConfigs.add(new Kakao());

        return tmpConfigs;
    }

    public List<Post> scrapPosts(List<BlogConfig> blogConfigs) throws ScrapException {
        int MAX_RETRIES = 3;
        long INITIAL_RETRY_DELAY_SEC = 2;
        long MAX_RETRY_DELAY_SEC = 3;

        for (int attempt = 1; attempt <= MAX_RETRIES; attempt++) {
            try {
                return parse(blogConfigs);
            } catch (ScrapException e) {
                logger.warn("시도 횟수 {} 실패: {}", attempt, e.getMessage());

                if (attempt >= MAX_RETRIES) {
                    logger.error("재시도 실패");
                    throw e;
                }

                // 지수 백오프: 재시도 간격을 두 배로 증가시킨다.
                long delay = Math.min(INITIAL_RETRY_DELAY_SEC * (long) Math.pow(2, attempt - 1), MAX_RETRY_DELAY_SEC);

                try {
                    TimeUnit.SECONDS.sleep(delay);
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                    throw new ScrapException(ie.toString(), ErrorMessage.THREAD_INTERRUPT_EXCEPTION);
                }
            }
        }

        throw new ScrapException("", ErrorMessage.UNEXPECTED_CONDITION_EXCEPTION);
    }

    private List<Post> parse(List<BlogConfig> blogConfigs) throws ScrapException {
        List<Post> scrapedPosts = new ArrayList<>();
        for (BlogConfig blogConfig : blogConfigs) {
            try {
                Document document = Jsoup.connect(blogConfig.getBlogUrl()).get();
                Elements items = document.select(blogConfig.getListTagName());
                if (items.isEmpty()) {
                    throw new ScrapParsingException(blogConfig.getBlogUrl());
                } else {
                    for (Element item : items) {
                        Post post = blogConfig.parseElement(item);
                        if (post.getTitle().isEmpty() || post.getLink().equals(blogConfig.getBlogUrl())) {
                            post.printPost();
                            throw new ScrapParsingException(blogConfig.getBlogUrl());
                        }
                        scrapedPosts.add(post);
                    }
                }
            } catch (UnknownHostException e2) {
                throw new ScrapHttpException(blogConfig.getBlogUrl());
            } catch (IOException e) {
                throw new ScrapException(e.getLocalizedMessage());
            }
        }

        return scrapedPosts;
    }

    public void savePosts(List<Post> scrapedPosts) {
        System.out.printf("스크랩한 게시글 개수: %d\n", scrapedPosts.size());
        List<String> scrapedLinks = scrapedPosts.stream()
                .map(Post::getLink)
                .toList();

        List<String> duplicateLinks = postRepository.findAllByLinkIn(scrapedLinks)
                .stream()
                .map(Post::getLink)
                .toList();

        System.out.printf("겹치는 게시글 개수: %d\n", duplicateLinks.size());

        List<Post> newPosts = scrapedPosts.stream()
                .filter(post -> !duplicateLinks.contains(post.getLink()))
                .toList();

        System.out.printf("새로운 게시글 개수: %d\n", newPosts.size());

        if (newPosts.isEmpty()) {
            System.out.println("저장할 새로운 포스트가 없습니다.");
            return;
        }
        printPosts(newPosts);
        saveNewPosts(newPosts);
    }

    private void printPosts(List<Post> posts) {
        for (Post post : posts) {
            System.out.println("\n포스트 저장됨: " + post.getLink());
            post.printPost();
        }
    }

    private void saveNewPosts(List<Post> newPosts) {
        postRepository.saveAll(newPosts);
        System.out.printf("%d 개의 포스트 저장됨\n", newPosts.size());
    }

    public void printMissingPostsCount(List<Post> scrapedPosts) {
        // 스크랩한 게시글의 링크 목록을 추출
        List<String> scrapedLinks = scrapedPosts.stream()
                .map(Post::getLink)
                .toList();

        // 데이터베이스에 있는 모든 게시글의 링크를 조회
        List<String> allLinksInDb = postRepository.findAll()
                .stream()
                .map(Post::getLink)
                .toList();

        // 데이터베이스에는 있지만 스크랩 결과에 없는 게시글의 링크 목록
        List<String> missingLinks = allLinksInDb.stream()
                .filter(link -> !scrapedLinks.contains(link))
                .toList();

        // 결과 출력
        for (var missingLink: missingLinks) {
            System.out.println(missingLink);
        }
        System.out.printf("스크랩 결과에 없는 게시글 개수: %d\n", missingLinks.size());
    }
}
