import React from 'react'
import { useNavigate } from 'react-router-dom'
import {
  HeroSection,
  HeroTitle,
  HeroSubtitle,
  CTAContainer,
  CTAButton,
  OutlineButton,
  SectionTitle,
  HowItWorks,
  Step,
  StepNumber,
  StepText,
  PricingSection,
  CardContainer,
  Card,
  Price,
  PriceTitle,
  QuoteSection,
  Quote
} from './styles'

const Home = () => {
  const navigate = useNavigate()
  return (
    <div>
      <HeroSection>
        <HeroTitle>A Song Made Just for Them.</HeroTitle>
        <HeroSubtitle>
          Funny, romantic, emotional – fully personalized songs for any occasion. You tell the story. We write the anthem.
        </HeroSubtitle>
        <CTAContainer>
          <CTAButton onClick={() => navigate('/packages')}>Get a Song</CTAButton>
          <OutlineButton>See Examples</OutlineButton>
        </CTAContainer>
      </HeroSection>

      <SectionTitle>How It Works</SectionTitle>
      <HowItWorks>
        <Step>
          <StepNumber>1</StepNumber>
          <StepText>Pick a song style: Love, Roast, Birthday, or Biz</StepText>
        </Step>
        <Step>
          <StepNumber>2</StepNumber>
          <StepText>Tell us about the person</StepText>
        </Step>
        <Step>
          <StepNumber>🎵</StepNumber>
          <StepText>Get a song that slaps harder than their last relationship 💀</StepText>
        </Step>
      </HowItWorks>

      <SectionTitle>Why People Love It</SectionTitle>
      <CardContainer>
        <Card>
          <PriceTitle>Short & Sweet</PriceTitle>
          <Price>€15</Price>
          <p>30–45s song<br />1 verse + hook</p>
        </Card>
        <Card>
          <PriceTitle>Full Package</PriceTitle>
          <Price>€29</Price>
          <p>60–75s song<br />Custom tone, extra detail</p>
        </Card>
        <Card>
          <PriceTitle>Business Ad</PriceTitle>
          <Price>€59–99</Price>
          <p>Commercial jingle<br />Custom beat rights</p>
        </Card>
      </CardContainer>

      <SectionTitle>Pricing</SectionTitle>
      <QuoteSection>
        <Quote>“Made my grandpa cry.”</Quote>
        <Quote>“My roommate couldn’t stop replaying it.”</Quote>
        <Quote>“Better than Cameo and way cheaper.”</Quote>
      </QuoteSection>
    </div>
  )
}

export default Home
