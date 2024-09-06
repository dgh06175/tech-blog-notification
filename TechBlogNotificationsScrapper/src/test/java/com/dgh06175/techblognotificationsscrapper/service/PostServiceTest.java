package com.dgh06175.techblognotificationsscrapper.service;

import static org.assertj.core.api.Assertions.assertThat;

import com.dgh06175.techblognotificationsscrapper.config.BlogConfig;
import com.dgh06175.techblognotificationsscrapper.config.html.Toss;
import com.dgh06175.techblognotificationsscrapper.config.rss.Kakao;
import com.dgh06175.techblognotificationsscrapper.config.rss.Woowahan;
import com.dgh06175.techblognotificationsscrapper.domain.Post;
import com.dgh06175.techblognotificationsscrapper.exception.ScrapException;
import com.dgh06175.techblognotificationsscrapper.repository.PostRepository;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

@SpringBootTest
@Transactional
class PostServiceTest {
    @Autowired
    private PostRepository postRepository;

    @Autowired
    private PostService postService;

    @Test
    void 블로그_설정_테스트() {
        List<BlogConfig> blogConfigs = postService.getBlogConfigs();
        assertThat(blogConfigs).hasSize(3);
        assertThat(blogConfigs).anyMatch(config -> config instanceof Toss);
        assertThat(blogConfigs).anyMatch(config -> config instanceof Kakao);
        assertThat(blogConfigs).anyMatch(config -> config instanceof Woowahan);
    }

    @Test
    void 게시글_스크랩_테스트() throws ScrapException {
        List<BlogConfig> blogConfigs = postService.getBlogConfigs();
        List<Post> posts = postService.scrapPosts(blogConfigs);
        assertThat(posts).isNotNull();
    }

    @Test
    void 게시글_저장_테스트() {
        List<Post> savedPosts = postRepository.findAll();
        int savedPostCount = savedPosts.size();

        Post post1 = new Post();
        post1.setLink("https://example.com/1");
        post1.setTitle("Test Post 1");

        Post post2 = new Post();
        post2.setLink("https://example.com/2");
        post2.setTitle("Test Post 2");

        List<Post> posts = List.of(post1, post2);
        postService.savePosts(posts);

        savedPosts = postRepository.findAll();
        assertThat(savedPosts).hasSize(savedPostCount + 2);
        assertThat(savedPosts).extracting(Post::getLink)
                .contains("https://example.com/1", "https://example.com/2");
    }
}