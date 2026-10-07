import { MLSystemsLab } from "./Lab";
import {
  additionalLearning,
  additionalPractice,
  capabilities,
  featuredProjects,
  profile,
  profileName
} from "./portfolio";

function ExternalLinks({ compact = false }: { compact?: boolean }) {
  const links = [
    { label: "GitHub", href: profile.github },
    { label: "Resume", href: profile.resume }
  ].filter((link) => link.href);

  return (
    <div className={compact ? "external-links compact" : "external-links"}>
      {links.map((link) => (
        <a key={link.label} href={link.href} target="_blank" rel="noreferrer">
          {link.label}
        </a>
      ))}
    </div>
  );
}

function App() {
  return (
    <div className="portfolio-shell">
      <header className="portfolio-header">
        <a className="portfolio-name" href="#top" aria-label="Back to top">
          {profileName}
        </a>

        <nav className="portfolio-nav" aria-label="Portfolio navigation">
          <a href="#about">About</a>
          <a href="#work">Work</a>
          <a href="#skills">Skills</a>
          <a href="#lab">Lab</a>
        </nav>

        <ExternalLinks compact />
      </header>

      <main id="top">
        <section className="hero-section">
          <p className="hero-role">{profile.role}</p>
          <h1>{profileName}</h1>
          <p className="hero-summary">{profile.summary}</p>

          <div className="hero-meta" aria-label="Profile details">
            <span>Innopolis University</span>
            <span>GPA 4.9 / 5.0</span>
            <span>{profile.location}</span>
          </div>

          <div className="hero-actions">
            <a className="primary-action" href="#work">Selected work</a>
            <a className="secondary-action" href="#lab">Interactive ML lab</a>
          </div>
        </section>

        <section className="portfolio-section about-section" id="about">
          <div className="section-heading">
            <h2>About</h2>
          </div>

          <div className="about-layout">
            <p className="about-copy">
              Second-year BSc student in Data Analysis and Artificial Intelligence at
              Innopolis University. GPA 4.9/5.0, full-tuition scholarship, with the
              programme taught entirely in English. Project work includes hybrid
              retrieval, Service Desk categorization and routing, and deploying multiple
              ML systems through FastAPI, React, Docker and CI.
            </p>

            <dl className="about-facts">
              <div>
                <dt>Education</dt>
                <dd>{profile.education}</dd>
              </div>
              <div>
                <dt>Status</dt>
                <dd>{profile.currentStatus}</dd>
              </div>
              <div>
                <dt>Contact</dt>
                <dd>
                  <a href={`mailto:${profile.email}`}>{profile.email}</a>
                  <br />
                  <a href={profile.telegram} target="_blank" rel="noreferrer">
                    Telegram
                  </a>
                </dd>
              </div>
            </dl>
          </div>
        </section>

        <section className="portfolio-section selected-work" id="work">
          <div className="section-heading">
            <h2>Selected work</h2>
            <p>
              Competition work, applied ML systems and a university team project,
              presented with the same results reported in the current resume.
            </p>
          </div>

          <div className="project-list">
            {featuredProjects.map((project) => (
              <article className="featured-project" key={project.id}>
                <div className="project-main">
                  <div className="project-title-row">
                    <h3>{project.title}</h3>
                  </div>

                  <p className="project-description">{project.description}</p>
                  <p className="project-approach">{project.approach}</p>

                  <div className="project-tech">
                    {project.technologies.join(", ")}
                  </div>

                  {(project.liveUrl || project.sourceUrl) && (
                    <div className="project-actions">
                      {project.liveUrl && <a href={project.liveUrl}>Open lab</a>}
                      {project.sourceUrl && (
                        <a href={project.sourceUrl} target="_blank" rel="noreferrer">
                          Source
                        </a>
                      )}
                    </div>
                  )}
                </div>

                <dl className="project-results" aria-label={`${project.title} results`}>
                  {project.metrics.map((metric) => (
                    <div key={metric.label}>
                      <dt>{metric.label}</dt>
                      <dd>{metric.value}</dd>
                    </div>
                  ))}
                </dl>
              </article>
            ))}
          </div>
        </section>

        <section className="portfolio-section skills-section" id="skills">
          <div className="section-heading">
            <h2>Skills</h2>
          </div>

          <div className="capability-grid">
            {capabilities.map((capability) => (
              <div className="capability-group" key={capability.title}>
                <h3>{capability.title}</h3>
                <p>{capability.items.join(", ")}</p>
              </div>
            ))}
          </div>

          <div className="learning-layout">
            <div>
              <h3>Additional education</h3>
              {additionalLearning.map((item) => <p key={item}>{item}</p>)}
            </div>
            <div>
              <h3>Additional practice</h3>
              {additionalPractice.map((item) => <p key={item}>{item}</p>)}
            </div>
          </div>
        </section>

        <MLSystemsLab />
      </main>

      <footer className="portfolio-footer">
        <span>{profileName}</span>
        <div>
          <a href={profile.github} target="_blank" rel="noreferrer">GitHub</a>
          <a href={profile.telegram} target="_blank" rel="noreferrer">Telegram</a>
          <a href={`mailto:${profile.email}`}>Email</a>
          <a href={profile.resume} target="_blank" rel="noreferrer">Resume</a>
        </div>
      </footer>
    </div>
  );
}

export default App;
