/**
 * Resolver Service
 * Handles the core matching engine functionality for TTrack Electron
 * Implements the transcript-curriculum comparison logic from the original TTrack
 */

/**
 * Match transcript courses with curriculum requirements
 * @param {Array} transcript - Transcript data with course details
 * @param {Array} curriculum - Curriculum data with course requirements
 * @returns {Object} Results containing matched courses, missing courses, and recommendations
 */
export const matchCourses = (transcript, curriculum) => {
  // Initialize results structure
  const results = {
    matchedCourses: [],
    missingCourses: [],
    recommendations: [],
    stats: {
      totalRequired: 0,
      totalCompleted: 0,
      percentageComplete: 0
    }
  };
  
  if (!transcript?.length || !curriculum?.length) {
    return results;
  }

  // Create a map of transcript courses for easier lookup
  const transcriptMap = new Map();
  transcript.forEach(course => {
    // Use course code or name as the key
    const key = course.CourseCode || course.Code || course.Course;
    if (key) {
      transcriptMap.set(key.trim().toUpperCase(), {
        ...course,
        Status: course.Grade === 'F' ? 'Failed' : 'Completed'
      });
    }
  });

  // Process curriculum requirements
  curriculum.forEach(requirement => {
    const reqCode = requirement.CourseCode || requirement.Code || requirement.Course;
    
    if (!reqCode) return;
    
    const reqCodeNormalized = reqCode.trim().toUpperCase();
    results.stats.totalRequired++;
    
    // Check if the requirement is satisfied in transcript
    if (transcriptMap.has(reqCodeNormalized)) {
      const transcriptCourse = transcriptMap.get(reqCodeNormalized);
      
      // Only count as matched if the course was passed
      if (transcriptCourse.Status === 'Completed') {
        results.matchedCourses.push({
          ...requirement,
          TranscriptGrade: transcriptCourse.Grade,
          Status: 'Done'
        });
        results.stats.totalCompleted++;
      } else {
        // Failed courses need to be retaken
        results.missingCourses.push({
          ...requirement,
          TranscriptGrade: transcriptCourse.Grade,
          Status: 'Failed'
        });
      }
    } else {
      // Course not found in transcript
      results.missingCourses.push({
        ...requirement,
        Status: 'Missing'
      });
    }
  });

  // Calculate percentage complete
  if (results.stats.totalRequired > 0) {
    results.stats.percentageComplete = Math.round(
      (results.stats.totalCompleted / results.stats.totalRequired) * 100
    );
  }

  // Generate recommendations
  results.recommendations = generateRecommendations(results.missingCourses);

  return results;
};

/**
 * Generate course recommendations based on missing courses
 * @param {Array} missingCourses - List of courses not completed
 * @returns {Array} Recommended courses to take next
 */
const generateRecommendations = (missingCourses) => {
  if (!missingCourses?.length) return [];
  
  // Prioritize core courses over electives
  const core = missingCourses.filter(course => 
    !course.Type?.toLowerCase().includes('elective'));
  
  const electives = missingCourses.filter(course => 
    course.Type?.toLowerCase().includes('elective'));
  
  // Simple recommendation algorithm - prioritize failed courses, then cores, then electives
  // More sophisticated version could consider prerequisites, course availability, etc.
  const failedCourses = missingCourses.filter(course => course.Status === 'Failed');
  
  const recommendations = [
    ...failedCourses,
    ...core.filter(c => !failedCourses.includes(c)).slice(0, 3),
    ...electives.slice(0, 2)
  ].slice(0, 5); // Limit to 5 recommendations
  
  return recommendations.map(course => ({
    ...course,
    RecommendationReason: course.Status === 'Failed' ? 
      'Previously attempted course - needs to be retaken' : 
      `Required ${course.Type || 'course'} for your program`
  }));
};
