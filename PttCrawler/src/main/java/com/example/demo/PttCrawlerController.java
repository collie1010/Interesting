package com.example.demo;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/ptt")
public class PttCrawlerController {

    @Autowired
    private PttCrawlerService pttCrawlerService;

    @GetMapping("/board/{boardName}")
    public ResponseEntity<List<ArticleDTO>> crawlBoard(@PathVariable String boardName) {
        try {
            List<ArticleDTO> articles = pttCrawlerService.crawlBoard(boardName);
            return ResponseEntity.ok(articles);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }
}

