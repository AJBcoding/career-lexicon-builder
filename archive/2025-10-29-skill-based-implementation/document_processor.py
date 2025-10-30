"""Document processing and classification for Career Lexicon Builder.

This module handles document type classification and text extraction from
uploaded career documents (resumes, cover letters, job descriptions).
"""

from enum import Enum
from typing import Tuple, Optional
from dataclasses import dataclass
import re


class DocumentType(Enum):
    """Document type classification."""
    RESUME = "resume"
    COVER_LETTER = "cover_letter"
    JOB_DESCRIPTION = "job_description"
    UNKNOWN = "unknown"


@dataclass
class ClassificationResult:
    """Result of document classification."""
    document_type: DocumentType
    confidence: float  # 0.0 to 1.0
    reasoning: str  # Explanation of classification


class DocumentClassifier:
    """Classifies career documents using heuristic patterns."""
    
    # Resume indicators
    RESUME_PATTERNS = [
        r'\b(education|experience|skills|work history)\b',
        r'\b(objective|summary|professional summary)\b',
        r'\b(bachelor|master|phd|b\.?a\.?|m\.?a\.?|b\.?s\.?|m\.?s\.?)\b',
        r'\b(certifications?|licenses?)\b',
        r'\b(references available|references upon request)\b',
        r'^\d{4}\s*[-â€"]\s*(\d{4}|present)',  # Date ranges like "2020 - 2023"
    ]
    
    # Cover letter indicators
    COVER_LETTER_PATTERNS = [
        r'\b(dear|to whom it may concern|hiring manager)\b',
        r'\b(sincerely|regards|best regards|yours truly)\b',
        r'\b(i am writing to|i am interested in|i would like to apply)\b',
        r'\b(my experience|my background|my skills)\b',
        r'\b(look forward to|opportunity to discuss|thank you for considering)\b',
        r'\b(position|role|opportunity)\s+(at|with)',
    ]
    
    # Job description indicators
    JOB_DESCRIPTION_PATTERNS = [
        r'\b(job description|position description|job posting)\b',
        r'\b(responsibilities|duties|requirements|qualifications)\b',
        r'\b(we are seeking|we are looking for|ideal candidate)\b',
        r'\b(must have|required|preferred)\b',
        r'\b(salary range|compensation|benefits)\b',
        r'\b(equal opportunity employer|eeo|diversity)\b',
        r'\b(apply|submit|application deadline)\b',
    ]
    
    def __init__(self, min_confidence: float = 0.6):
        """Initialize classifier.
        
        Args:
            min_confidence: Minimum confidence threshold for classification
        """
        self.min_confidence = min_confidence
    
    def classify(self, text: str) -> ClassificationResult:
        """Classify a document based on its text content.
        
        Args:
            text: Document text content
            
        Returns:
            ClassificationResult with type, confidence, and reasoning
        """
        if not text or len(text.strip()) < 50:
            return ClassificationResult(
                document_type=DocumentType.UNKNOWN,
                confidence=0.0,
                reasoning="Text too short for reliable classification"
            )
        
        # Normalize text for pattern matching
        text_lower = text.lower()
        
        # Count pattern matches for each document type
        resume_score = self._count_pattern_matches(text_lower, self.RESUME_PATTERNS)
        cover_letter_score = self._count_pattern_matches(text_lower, self.COVER_LETTER_PATTERNS)
        job_desc_score = self._count_pattern_matches(text_lower, self.JOB_DESCRIPTION_PATTERNS)
        
        # Calculate total matches
        total_matches = resume_score + cover_letter_score + job_desc_score
        
        if total_matches == 0:
            return ClassificationResult(
                document_type=DocumentType.UNKNOWN,
                confidence=0.0,
                reasoning="No characteristic patterns found"
            )
        
        # Determine document type and confidence
        scores = [
            (DocumentType.RESUME, resume_score),
            (DocumentType.COVER_LETTER, cover_letter_score),
            (DocumentType.JOB_DESCRIPTION, job_desc_score)
        ]
        scores.sort(key=lambda x: x[1], reverse=True)
        
        top_type, top_score = scores[0]
        second_score = scores[1][1]
        
        # Calculate confidence based on:
        # 1. Proportion of matches for top type
        # 2. Margin between top and second type
        proportion = top_score / total_matches
        margin = (top_score - second_score) / total_matches if total_matches > 0 else 0
        
        # Weight proportion more heavily but consider margin
        confidence = (proportion * 0.7) + (margin * 0.3)
        
        # Apply heuristics to refine confidence
        confidence = self._apply_heuristics(text_lower, top_type, confidence)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(top_type, top_score, second_score, confidence)
        
        # Check minimum confidence threshold
        if confidence < self.min_confidence:
            return ClassificationResult(
                document_type=DocumentType.UNKNOWN,
                confidence=confidence,
                reasoning=f"Confidence too low: {reasoning}"
            )
        
        return ClassificationResult(
            document_type=top_type,
            confidence=confidence,
            reasoning=reasoning
        )
    
    def _count_pattern_matches(self, text: str, patterns: list) -> int:
        """Count total pattern matches in text.
        
        Args:
            text: Text to search (already lowercased)
            patterns: List of regex patterns
            
        Returns:
            Total number of matches found
        """
        count = 0
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            count += len(matches)
        return count
    
    def _apply_heuristics(self, text: str, doc_type: DocumentType, confidence: float) -> float:
        """Apply additional heuristics to refine confidence score.
        
        Args:
            text: Document text (lowercased)
            doc_type: Classified document type
            confidence: Initial confidence score
            
        Returns:
            Adjusted confidence score
        """
        adjusted = confidence
        
        # Resume heuristics
        if doc_type == DocumentType.RESUME:
            # Check for date ranges (common in resumes)
            if re.search(r'\d{4}\s*[-â€"]\s*\d{4}', text):
                adjusted += 0.05
            # Check for education section
            if re.search(r'\b(education|academic)\b.*\b(university|college|school)\b', text):
                adjusted += 0.05
        
        # Cover letter heuristics
        elif doc_type == DocumentType.COVER_LETTER:
            # Check for salutation
            if re.search(r'^(dear|hello|hi|greetings)', text):
                adjusted += 0.1
            # Check for signature
            if re.search(r'(sincerely|regards|yours truly|best wishes)', text):
                adjusted += 0.1
            # Check for first-person narrative
            first_person = len(re.findall(r'\b(i|my|me)\b', text))
            if first_person > 10:  # Threshold for first-person usage
                adjusted += 0.05
        
        # Job description heuristics
        elif doc_type == DocumentType.JOB_DESCRIPTION:
            # Check for company/employer language
            if re.search(r'\b(we|our company|our team|our organization)\b', text):
                adjusted += 0.05
            # Check for application instructions
            if re.search(r'\b(apply|submit|send|email)\b.*\b(resume|cv|application)\b', text):
                adjusted += 0.1
        
        # Cap confidence at 1.0
        return min(adjusted, 1.0)
    
    def _generate_reasoning(
        self, 
        doc_type: DocumentType, 
        top_score: int, 
        second_score: int,
        confidence: float
    ) -> str:
        """Generate human-readable reasoning for classification.
        
        Args:
            doc_type: Classified document type
            top_score: Match score for top type
            second_score: Match score for second-place type
            confidence: Final confidence score
            
        Returns:
            Reasoning string
        """
        margin = top_score - second_score
        
        if confidence >= 0.8:
            strength = "strong"
        elif confidence >= 0.6:
            strength = "moderate"
        else:
            strength = "weak"
        
        reasoning = (
            f"Classified as {doc_type.value} with {strength} confidence ({confidence:.2f}). "
            f"Found {top_score} characteristic patterns."
        )
        
        if margin < 2:
            reasoning += " Classification was close; document has mixed characteristics."
        
        return reasoning


class DocumentProcessor:
    """Main processor for handling career documents."""
    
    def __init__(self, min_confidence: float = 0.6):
        """Initialize document processor.
        
        Args:
            min_confidence: Minimum confidence for classification
        """
        self.classifier = DocumentClassifier(min_confidence=min_confidence)
    
    def process_document(self, text: str, filename: Optional[str] = None) -> dict:
        """Process a document and return classification and metadata.
        
        Args:
            text: Document text content
            filename: Optional filename for additional context
            
        Returns:
            Dictionary containing classification results and metadata
        """
        # Classify document
        classification = self.classifier.classify(text)
        
        # Build result dictionary
        result = {
            'document_type': classification.document_type.value,
            'confidence': classification.confidence,
            'reasoning': classification.reasoning,
            'text_length': len(text),
            'filename': filename
        }
        
        return result
