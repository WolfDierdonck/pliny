package main

import (
	"sync"
	"time"
)

type RateLimiter struct {
	mu       sync.Mutex
	requests []time.Time
	limit    int
	window   time.Duration
}

func NewRateLimiter(limit int, window time.Duration) RateLimiter {
	return RateLimiter{
		limit:  limit,
		window: window,
	}
}

func (rl *RateLimiter) Allow() bool {
	rl.mu.Lock()
	defer rl.mu.Unlock()

	now := time.Now()

	// Remove outdated requests from the window
	cutoff := now.Add(-rl.window)
	newRequests := rl.requests[:0] // Reuse the same slice memory
	for _, t := range rl.requests {
		if t.After(cutoff) {
			newRequests = append(newRequests, t)
		}
	}
	rl.requests = newRequests

	// Allow if within limit
	if len(rl.requests) < rl.limit {
		rl.requests = append(rl.requests, now)
		return true
	}
	return false
}
