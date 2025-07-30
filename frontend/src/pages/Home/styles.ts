import styled from 'styled-components'

export const HeroSection = styled.section`
  padding: 2rem 1rem;
  text-align: center;
`

export const HeroTitle = styled.h1`
  font-size: 2rem;
  font-weight: 800;
  color: ${({ theme }) => theme.text};
`

export const HeroSubtitle = styled.p`
  margin-top: 1rem;
  color: ${({ theme }) => theme.secondary};
  font-size: 1rem;
  max-width: 600px;
  margin-inline: auto;
`

export const CTAContainer = styled.div`
  margin-top: 1.5rem;
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
`

export const CTAButton = styled.button`
  background: #ec4899;
  color: white;
  padding: 0.8rem 1.5rem;
  font-weight: bold;
  border-radius: 8px;
  border: none;
  cursor: pointer;
`

export const OutlineButton = styled(CTAButton)`
  background: transparent;
  border: 1px solid #ec4899;
  color: #ec4899;
`

export const SectionTitle = styled.h2`
  font-size: 1.5rem;
  margin: 2rem 0 1rem;
  text-align: center;
`

export const HowItWorks = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 0 1.5rem;
`

export const Step = styled.div`
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
`

export const StepNumber = styled.div`
  background: #6b21a8;
  color: white;
  font-weight: bold;
  padding: 0.5rem;
  border-radius: 999px;
  min-width: 2rem;
  text-align: center;
`

export const StepText = styled.p`
  flex: 1;
  margin: 0;
`

export const PricingSection = styled.section`
  margin-top: 2rem;
`

export const CardContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 0 1.5rem;

  @media (min-width: 768px) {
    flex-direction: row;
    justify-content: center;
  }
`

export const Card = styled.div`
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  border-radius: 12px;
  padding: 1rem;
  flex: 1;
  text-align: center;
  color: ${({ theme }) => theme.text};
`

export const PriceTitle = styled.h3`
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
`

export const Price = styled.div`
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
`

export const QuoteSection = styled.div`
  margin: 2rem 0;
  padding: 0 1rem;
  text-align: center;
`

export const Quote = styled.p`
  font-style: italic;
  margin: 0.5rem 0;
`
