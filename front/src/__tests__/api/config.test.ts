import { describe, it, expect } from 'vitest';
import { API_BASE_URL, API_ROUTES } from '../../lib/api/config';

describe('API Configuration', () => {
  it('should have a valid API_BASE_URL', () => {
    expect(API_BASE_URL).toBeDefined();
    expect(typeof API_BASE_URL).toBe('string');
    expect(API_BASE_URL).toMatch(/^https?:\/\//); // Should start with http:// or https://
  });

  it('should have all expected API routes defined', () => {
    // Auth routes
    expect(API_ROUTES.auth.register).toBe('/api/auth/register');
    expect(API_ROUTES.auth.login).toBe('/api/auth/login');
    expect(API_ROUTES.auth.socialLogin).toBe('/api/auth/social-login');
    expect(API_ROUTES.auth.profile).toBe('/api/users/profile');

    // Character routes
    expect(API_ROUTES.characters.base).toBe('/api/characters');
    expect(API_ROUTES.characters.detail('test-id')).toBe('/api/characters/test-id');

    // Artifact routes
    expect(API_ROUTES.artifacts.base).toBe('/api/artifacts');
    expect(API_ROUTES.artifacts.characterArtifacts('char-id')).toBe('/api/artifacts/characters/char-id/artifacts');
    expect(API_ROUTES.artifacts.characterArtifact('char-id', 'art-id')).toBe('/api/artifacts/characters/char-id/artifacts/art-id');

    // Personality routes
    expect(API_ROUTES.personality.questions).toBe('/api/personality/questions');
    expect(API_ROUTES.personality.results).toBe('/api/personality/results');

    // Adventure routes
    expect(API_ROUTES.adventure.story).toBe('/api/adventure/story');
    expect(API_ROUTES.adventure.progress).toBe('/api/adventure/progress');

    // Health check
    expect(API_ROUTES.health).toBe('/api/health');
  });
}); 