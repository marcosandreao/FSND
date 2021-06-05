import React, { Component } from 'react';

import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

class QuestionView extends Component {
  constructor(){
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: [],
      currentCategory: null,
    }
  }

  componentDidMount() {
    this.listCategories();
  }

  catById = (catId) => this.state.categories.filter(f=>f.id == catId)[0];

  getQuestions = () => {
    let query = this.state.searchTerm? this.state.searchTerm : '';
    $.ajax({
      url: `/questions?page=${this.state.page}&search_term=${query}`, 
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.data,
          totalQuestions: result.total,
          currentCategory:  this.state.categories[0].type })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  selectPage(num) {
    this.setState({page: num}, () => this.getQuestions());
  }

  createPagination(){
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10)
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => {this.selectPage(i)}}>{i}
        </span>)
    }
    return pageNumbers;
  }

  getByCategory= (id) => {
    this.searchTerm = null;
    $.ajax({
      url: `/categories/${id}/questions`, 
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.data,
          totalQuestions: result.total,
          currentCategory: this.catById(id).type
         })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  listCategories = (id) => {
    $.ajax({
      url: `/categories`,
      type: "GET",
      success: (result) => {
        this.setState({
          categories: result.data
        });
        this.getQuestions();
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  submitSearch = (searchTerm) => {
    this.state.searchTerm = searchTerm;
    $.ajax({
      url: `/questions?search_term=${searchTerm}`, 
      type: "GET",
      dataType: 'json',
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          questions: result.data,
          totalQuestions: result.total })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  questionAction = (id) => (action) => {
    if(action === 'DELETE') {
      if(window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: `/questions/${id}`,
          type: "DELETE",
          success: (result) => {
            this.getQuestions();
          },
          error: (error) => {
            alert('Unable to load questions. Please try your request again')
            return;
          }
        })
      }
    }
  }

  listQuestions = () => {
    this.searchTerm = null;
    this.getQuestions();
  }

  render() {
    return (
      <div className="question-view">
        <div className="categories-list">
          <h2 onClick={() => {this.listQuestions()}}>Categories</h2>
          <ul>
          {this.state.categories.map((cat, ) => (
              <li key={cat.id} onClick={() => {this.getByCategory(cat.id)}}>
                {cat.type}
                <img className="category" src={`${cat.type.toLowerCase()}.svg`}/>
              </li>
            ))}
          </ul>
          <Search submitSearch={this.submitSearch}/>
        </div>
        <div className="questions-list">
          <h2>Questions</h2>
          {this.state.questions.map((q, ind) => (
            <Question
              key={q.id}
              question={q.question}
              answer={q.answer}
              category={this.catById(q.category).type} 
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
            />
          ))}
          <div className="pagination-menu">
            {this.createPagination()}
          </div>
        </div>

      </div>
    );
  }
}

export default QuestionView;
