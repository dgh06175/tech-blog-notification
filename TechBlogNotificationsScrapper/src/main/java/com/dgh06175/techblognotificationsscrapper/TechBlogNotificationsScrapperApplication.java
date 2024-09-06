package com.dgh06175.techblognotificationsscrapper;

import com.dgh06175.techblognotificationsscrapper.controller.ScrapController;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

@EnableJpaAuditing
@SpringBootApplication
public class TechBlogNotificationsScrapperApplication {

    public static void main(String[] args) {
        SpringApplication.run(TechBlogNotificationsScrapperApplication.class, args);
    }

    @Bean
    CommandLineRunner runScraper(ScrapController scrapController) {
        return args -> {
            scrapController.run();
        };
    }
}


